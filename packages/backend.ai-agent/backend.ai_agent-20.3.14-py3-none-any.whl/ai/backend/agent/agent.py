from __future__ import annotations

from abc import ABCMeta, abstractmethod
import asyncio
from collections import defaultdict
from decimal import Decimal
from io import BytesIO, SEEK_END
import logging
from pathlib import Path
import pickle
import re
import signal
import time
from typing import (
    Any,
    AsyncIterator,
    Collection,
    Dict,
    FrozenSet,
    Optional,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
    Set,
    Tuple,
    Union,
    TYPE_CHECKING,
    cast,
)

import aioredis
import aiotools
from async_timeout import timeout
import attr
import snappy
import zmq, zmq.asyncio

from ai.backend.common import msgpack, redis
from ai.backend.common.docker import (
    ImageRef,
    MIN_KERNELSPEC,
    MAX_KERNELSPEC,
)
from ai.backend.common.logging import BraceStyleAdapter
from ai.backend.common.types import (
    aobject,
    # TODO: eliminate use of ContainerId
    ContainerId, KernelId,
    DeviceName, SlotName,
    AutoPullBehavior, ImageRegistry,
    KernelCreationConfig,
    KernelCreationResult,
    Sentinel,
)
from ai.backend.common.utils import current_loop
from ai.backend.common.plugin.monitor import ErrorPluginContext, StatsPluginContext
from . import __version__ as VERSION
from .defs import ipc_base_path
from .kernel import AbstractKernel
from .resources import (
    AbstractComputeDevice,
    AbstractComputePlugin,
    AbstractAllocMap,
)
from .stats import (
    StatContext, StatModes,
)
from .types import (
    Container,
    ContainerStatus,
    ContainerLifecycleEvent,
    LifecycleEvent,
)
from .utils import generate_agent_id

if TYPE_CHECKING:
    from ai.backend.common.etcd import AsyncEtcd

log = BraceStyleAdapter(logging.getLogger('ai.backend.agent.agent'))

_sentinel = Sentinel.TOKEN

ACTIVE_STATUS_SET = frozenset([
    ContainerStatus.RUNNING,
    ContainerStatus.RESTARTING,
    ContainerStatus.PAUSED,
])

DEAD_STATUS_SET = frozenset([
    ContainerStatus.EXITED,
    ContainerStatus.DEAD,
    ContainerStatus.REMOVING,
])


@attr.s(auto_attribs=True, slots=True)
class RestartTracker:
    request_lock: asyncio.Lock
    destroy_event: asyncio.Event
    done_event: asyncio.Event


@attr.s(auto_attribs=True, slots=True)
class ComputerContext:
    instance: AbstractComputePlugin
    devices: Collection[AbstractComputeDevice]
    alloc_map: AbstractAllocMap


class AbstractAgent(aobject, metaclass=ABCMeta):

    loop: asyncio.AbstractEventLoop
    local_config: Mapping[str, Any]
    etcd: AsyncEtcd
    agent_id: str
    kernel_registry: MutableMapping[KernelId, AbstractKernel]
    computers: MutableMapping[str, ComputerContext]
    images: Mapping[str, str]
    port_pool: Set[int]

    redis: aioredis.Redis
    zmq_ctx: zmq.asyncio.Context

    terminating_kernels: Set[KernelId]
    restarting_kernels: MutableMapping[KernelId, RestartTracker]
    timer_tasks: MutableSequence[asyncio.Task]
    container_lifecycle_queue: 'asyncio.Queue[Union[ContainerLifecycleEvent, Sentinel]]'

    stat_ctx: StatContext
    stat_sync_sockpath: Path
    stat_sync_task: asyncio.Task

    stats_monitor: StatsPluginContext
    error_monitor: ErrorPluginContext

    _pending_creation_tasks: Dict[str, Set[asyncio.Task]]

    def __init__(
        self,
        etcd: AsyncEtcd,
        local_config: Mapping[str, Any],
        *,
        stats_monitor: StatsPluginContext,
        error_monitor: ErrorPluginContext,
        skip_initial_scan: bool = False,
    ) -> None:
        self._skip_initial_scan = skip_initial_scan
        self.loop = current_loop()
        self.etcd = etcd
        self.local_config = local_config
        self.agent_id = generate_agent_id(__file__)
        self.kernel_registry = {}
        self.computers = {}
        self.images = {}  # repoTag -> digest
        self.terminating_kernels = set()
        self.restarting_kernels = {}
        self.stat_ctx = StatContext(
            self, mode=StatModes(local_config['container']['stats-type']),
        )
        self.timer_tasks = []
        self.port_pool = set(range(
            local_config['container']['port-range'][0],
            local_config['container']['port-range'][1] + 1,
        ))
        self.stats_monitor = stats_monitor
        self.error_monitor = error_monitor
        self._rx_distro = re.compile(r"\.([a-z-]+\d+\.\d+)\.")
        self._pending_creation_tasks = defaultdict(set)

    async def __ainit__(self) -> None:
        """
        An implementation of AbstractAgent would define its own ``__ainit__()`` method.
        It must call this super method in an appropriate order, only once.
        """
        self.resource_lock = asyncio.Lock()
        self.container_lifecycle_queue = asyncio.Queue()
        self.producer_lock = asyncio.Lock()
        self.redis_producer_pool = await redis.connect_with_retries(
            self.local_config['redis']['addr'].as_sockaddr(),
            db=4,  # REDIS_STREAM_DB in gateway.defs
            password=(self.local_config['redis']['password']
                      if self.local_config['redis']['password'] else None),
            encoding=None,
        )
        self.redis_stat_pool = await redis.connect_with_retries(
            self.local_config['redis']['addr'].as_sockaddr(),
            db=0,  # REDIS_STAT_DB in backend.ai-manager
            password=(self.local_config['redis']['password']
                      if self.local_config['redis']['password'] else None),
            encoding='utf8',
        )

        ipc_base_path.mkdir(parents=True, exist_ok=True)
        self.zmq_ctx = zmq.asyncio.Context()

        computers, self.slots = await self.detect_resources()
        for name, computer in computers.items():
            devices = await computer.list_devices()
            alloc_map = await computer.create_alloc_map()
            self.computers[name] = ComputerContext(computer, devices, alloc_map)

        if not self._skip_initial_scan:
            self.images = await self.scan_images()
            self.timer_tasks.append(aiotools.create_timer(self._scan_images_wrapper, 20.0))
            await self.scan_running_kernels()

        # Prepare stat collector tasks.
        self.timer_tasks.append(aiotools.create_timer(self.collect_node_stat, 5.0))
        self.timer_tasks.append(aiotools.create_timer(self.collect_container_stat, 5.0))

        # Prepare heartbeats.
        self.timer_tasks.append(aiotools.create_timer(self.heartbeat, 3.0))

        # Prepare auto-cleaning of idle kernels.
        self.timer_tasks.append(aiotools.create_timer(self.sync_container_lifecycles, 10.0))

        loop = current_loop()
        self.container_lifecycle_handler = loop.create_task(self.process_lifecycle_events())

        # Notify the gateway.
        await self.produce_event('instance_started', 'self-started')

    async def shutdown(self, stop_signal: signal.Signals) -> None:
        """
        An implementation of AbstractAgent would define its own ``shutdown()`` method.
        It must call this super method in an appropriate order, only once.
        """
        # Close all pending kernel runners.
        for kernel_obj in self.kernel_registry.values():
            if kernel_obj.runner is not None:
                await kernel_obj.runner.close()
            await kernel_obj.close()
        if stop_signal == signal.SIGTERM:
            await self.clean_all_kernels(blocking=True)

        # Stop timers.
        for task in self.timer_tasks:
            task.cancel()
        timer_cancel_results = await asyncio.gather(*self.timer_tasks, return_exceptions=True)
        for result in timer_cancel_results:
            if isinstance(result, Exception):
                log.error('timer cancellation error: {}', result)

        # Stop lifecycle event handler.
        await self.container_lifecycle_queue.put(_sentinel)
        await self.container_lifecycle_handler

        # Notify the gateway.
        await self.produce_event('instance_terminated', 'shutdown')

        # Close Redis connection pools.
        self.redis_producer_pool.close()
        await self.redis_producer_pool.wait_closed()
        self.redis_stat_pool.close()
        await self.redis_stat_pool.wait_closed()

        self.zmq_ctx.term()

    async def produce_event(self, event_name: str, *args) -> None:
        """
        Send an event to the manager(s).
        """
        if self.local_config['debug']['log-heartbeats']:
            _log = log.debug if event_name == 'instance_heartbeat' else log.info
        else:
            _log = (lambda *args: None) if event_name == 'instance_heartbeat' else log.info
        if event_name.startswith('kernel_') and len(args) > 0:
            _log('produce_event({0}, k:{1})', event_name, args[0])
        else:
            _log('produce_event({0})', event_name)
        encoded_event = msgpack.packb({
            'event_name': event_name,
            'agent_id': self.local_config['agent']['id'],
            'args': args,
        })
        if event_name == 'kernel_terminated':
            kernel_id = args[0]
            pending_creation_tasks = self._pending_creation_tasks.get(kernel_id, None)
            if pending_creation_tasks is not None:
                for t in pending_creation_tasks:
                    t.cancel()
        async with self.producer_lock:
            def _pipe_builder():
                pipe = self.redis_producer_pool.pipeline()
                pipe.rpush('events.prodcons', encoded_event)
                pipe.publish('events.pubsub', encoded_event)
                return pipe
            await redis.execute_with_retries(_pipe_builder)

    async def heartbeat(self, interval: float):
        """
        Send my status information and available kernel images to the manager(s).
        """
        res_slots = {}
        for cctx in self.computers.values():
            for slot_key, slot_type in cctx.instance.slot_types:
                res_slots[slot_key] = (
                    slot_type,
                    str(self.slots.get(slot_key, 0)),
                )
        agent_info = {
            'ip': str(self.local_config['agent']['rpc-listen-addr'].host),
            'region': self.local_config['agent']['region'],
            'scaling_group': self.local_config['agent']['scaling-group'],
            'addr': f"tcp://{self.local_config['agent']['rpc-listen-addr']}",
            'resource_slots': res_slots,
            'version': VERSION,
            'compute_plugins': {
                key: {
                    'version': computer.instance.get_version(),
                    **(await computer.instance.extra_info())
                }
                for key, computer in self.computers.items()
            },
            'images': snappy.compress(msgpack.packb([
                (repo_tag, digest) for repo_tag, digest in self.images.items()
            ])),
        }
        try:
            await self.produce_event('instance_heartbeat', agent_info)
        except asyncio.TimeoutError:
            log.warning('event dispatch timeout: instance_heartbeat')
        except Exception:
            log.exception('instance_heartbeat failure')
            await self.error_monitor.capture_exception()

    async def collect_logs(
        self,
        kernel_id: KernelId,
        container_id: str,
        async_log_iterator: AsyncIterator[bytes],
    ) -> None:
        chunk_size = self.local_config['agent']['container-logs']['chunk-size']
        log_key = f'containerlog.{container_id}'
        log_length = 0
        chunk_buffer = BytesIO()
        chunk_length = 0
        try:
            async for fragment in async_log_iterator:
                fragment_length = len(fragment)
                chunk_buffer.write(fragment)
                chunk_length += fragment_length
                log_length += fragment_length
                while chunk_length >= chunk_size:
                    cb = chunk_buffer.getbuffer()
                    stored_chunk = bytes(cb[:chunk_size])
                    await redis.execute_with_retries(
                        lambda: self.redis_producer_pool.rpush(
                            log_key, stored_chunk)
                    )
                    remaining = cb[chunk_size:]
                    chunk_length = len(remaining)
                    next_chunk_buffer = BytesIO(remaining)
                    next_chunk_buffer.seek(0, SEEK_END)
                    del remaining, cb
                    chunk_buffer.close()
                    chunk_buffer = next_chunk_buffer
            assert chunk_length < chunk_size
            if chunk_length > 0:
                await redis.execute_with_retries(
                    lambda: self.redis_producer_pool.rpush(
                        log_key, chunk_buffer.getvalue())
                )
        finally:
            chunk_buffer.close()
        # Keep the log for at most one hour in Redis.
        # This is just a safety measure to prevent memory leak in Redis
        # for cases when the event delivery has failed or processing
        # the log data has failed.
        await redis.execute_with_retries(
            lambda: self.redis_producer_pool.expire(log_key, 3600.0)
        )
        await self.produce_event(
            'kernel_log', str(kernel_id), container_id
        )

    async def collect_node_stat(self, interval: float):
        if self.local_config['debug']['log-stats']:
            log.debug('collecting node statistics')
        try:
            await self.stat_ctx.collect_node_stat()
        except asyncio.CancelledError:
            pass
        except Exception:
            log.exception('unhandled exception while syncing node stats')
            await self.error_monitor.capture_exception()

    async def collect_container_stat(self, interval: float):
        if self.local_config['debug']['log-stats']:
            log.debug('collecting container statistics')
        try:
            updated_kernel_ids = []
            container_ids = []
            for kernel_id, kernel_obj in [*self.kernel_registry.items()]:
                if not kernel_obj.stats_enabled:
                    continue
                updated_kernel_ids.append(kernel_id)
                container_ids.append(kernel_obj['container_id'])
            await self.stat_ctx.collect_container_stat(container_ids)
            # Let the manager store the statistics in the persistent database.
            if updated_kernel_ids:
                await self.produce_event('kernel_stat_sync',
                                         ','.join(map(str, updated_kernel_ids)))
        except asyncio.CancelledError:
            pass
        except Exception:
            log.exception('unhandled exception while syncing container stats')
            await self.error_monitor.capture_exception()

    async def _handle_start_event(self, ev: ContainerLifecycleEvent) -> None:
        kernel_obj = self.kernel_registry.get(ev.kernel_id)
        if kernel_obj is not None:
            kernel_obj.stats_enabled = True

    async def _handle_destroy_event(self, ev: ContainerLifecycleEvent) -> None:
        result = None
        try:
            kernel_obj = self.kernel_registry.get(ev.kernel_id)
            if kernel_obj is None:
                log.warning('destroy_kernel(k:{0}) kernel missing (already dead?)',
                            ev.kernel_id)
                if ev.container_id is None:
                    await self.rescan_resource_usage()
                    await self.produce_event(
                        'kernel_terminated', str(ev.kernel_id),
                        'already-terminated', None,
                    )
                    return
                else:
                    self.container_lifecycle_queue.put_nowait(
                        ContainerLifecycleEvent(
                            ev.kernel_id,
                            ev.container_id,
                            LifecycleEvent.CLEAN,
                            ev.reason,
                        )
                    )
            else:
                kernel_obj.stats_enabled = False
                kernel_obj.termination_reason = ev.reason
                if kernel_obj.runner is not None:
                    await kernel_obj.runner.close()
            result = await self.destroy_kernel(ev.kernel_id, ev.container_id)
        except Exception:
            log.exception('unhandled exception while processing DESTROY event')
            await self.error_monitor.capture_exception()
        finally:
            if ev.done_event is not None:
                ev.done_event.set()
                setattr(ev.done_event, '_result', result)

    async def _handle_clean_event(self, ev: ContainerLifecycleEvent) -> None:
        result = None
        try:
            kernel_obj = self.kernel_registry.get(ev.kernel_id)
            if kernel_obj is not None and kernel_obj.runner is not None:
                await kernel_obj.runner.close()
            result = await self.clean_kernel(
                ev.kernel_id,
                ev.container_id,
                ev.kernel_id in self.restarting_kernels,
            )
        except Exception:
            log.exception('unhandled exception while processing CLEAN event')
            await self.error_monitor.capture_exception()
        finally:
            try:
                kernel_obj = self.kernel_registry.get(ev.kernel_id)
                if kernel_obj is not None:
                    # Restore used ports to the port pool.
                    port_range = self.local_config['container']['port-range']
                    restored_ports = [*filter(
                        lambda p: port_range[0] <= p <= port_range[1],
                        kernel_obj['host_ports']
                    )]
                    self.port_pool.update(restored_ports)
                    await kernel_obj.close()
                    # Notify cleanup waiters.
                    if kernel_obj.clean_event is not None:
                        kernel_obj.clean_event.set()
                    # Forget.
                    self.kernel_registry.pop(ev.kernel_id, None)
            finally:
                if ev.done_event is not None:
                    ev.done_event.set()
                    setattr(ev.done_event, '_result', result)
                if ev.kernel_id in self.restarting_kernels:
                    self.restarting_kernels[ev.kernel_id].destroy_event.set()
                else:
                    await self.rescan_resource_usage()
                    await self.produce_event(
                        'kernel_terminated', str(ev.kernel_id),
                        ev.reason, None,
                    )

    async def process_lifecycle_events(self) -> None:
        async with aiotools.TaskGroup() as tg:
            while True:
                ev = await self.container_lifecycle_queue.get()
                if isinstance(ev, Sentinel):
                    with open(ipc_base_path / f'last_registry.{self.agent_id}.dat', 'wb') as f:
                        pickle.dump(self.kernel_registry, f)
                    return
                # attr currently does not support customizing getstate/setstate dunder methods
                # until the next release.
                log.info(f'lifecycle event: {ev!r}')
                try:
                    if ev.event == LifecycleEvent.START:
                        tg.create_task(self._handle_start_event(ev))
                    elif ev.event == LifecycleEvent.DESTROY:
                        tg.create_task(self._handle_destroy_event(ev))
                    elif ev.event == LifecycleEvent.CLEAN:
                        tg.create_task(self._handle_clean_event(ev))
                    else:
                        log.warning('unsupported lifecycle event: {!r}', ev)
                except Exception:
                    log.exception('unexpected error in process_lifecycle_events(), continuing...')
                finally:
                    self.container_lifecycle_queue.task_done()

    async def inject_container_lifecycle_event(
        self,
        kernel_id: KernelId,
        event: LifecycleEvent,
        reason: str,
        *,
        container_id: ContainerId = None,
        exit_code: int = None,
        done_event: asyncio.Event = None,
        clean_event: asyncio.Event = None,
    ) -> None:
        try:
            kernel_obj = self.kernel_registry[kernel_id]
            if kernel_obj.termination_reason:
                reason = kernel_obj.termination_reason
            if kernel_obj.clean_event is not None:
                # This should not happen!
                log.warning('overwriting kernel_obj.clean_event (k:{})', kernel_id)
            kernel_obj.clean_event = clean_event
            if container_id is not None and container_id != kernel_obj['container_id']:
                # This should not happen!
                log.warning('container id mismatch for kernel_obj (k:{}, c:{}) with event (c:{})',
                            kernel_id, kernel_obj['container_id'], container_id)
            container_id = kernel_obj['container_id']
        except KeyError:
            pass
        self.container_lifecycle_queue.put_nowait(
            ContainerLifecycleEvent(
                kernel_id,
                container_id,
                event,
                reason,
                done_event,
                exit_code,
            )
        )

    @abstractmethod
    async def enumerate_containers(
        self,
        status_filter: FrozenSet[ContainerStatus] = ACTIVE_STATUS_SET,
    ) -> Sequence[Tuple[KernelId, Container]]:
        """
        Enumerate the containers with the given status filter.
        """

    async def rescan_resource_usage(self) -> None:
        async with self.resource_lock:
            for computer_set in self.computers.values():
                computer_set.alloc_map.clear()
            for kernel_id, container in (await self.enumerate_containers()):
                for computer_set in self.computers.values():
                    await computer_set.instance.restore_from_container(
                        container,
                        computer_set.alloc_map,
                    )

    async def sync_container_lifecycles(self, interval: float) -> None:
        """
        Periodically synchronize the alive/known container sets,
        for cases when we miss the container lifecycle events from the underlying implementation APIs
        due to the agent restarts or crashes.
        """
        now = time.monotonic()
        known_kernels: Dict[KernelId, ContainerId] = {}
        alive_kernels: Dict[KernelId, ContainerId] = {}
        terminated_kernels = {}

        async with self.resource_lock:
            try:
                # Check if: there are dead containers
                for kernel_id, container in (await self.enumerate_containers(DEAD_STATUS_SET)):
                    if kernel_id in self.restarting_kernels:
                        continue
                    log.info('detected dead container during lifeycle sync (k:{0}, c:{})',
                            kernel_id, container.id)
                    terminated_kernels[kernel_id] = ContainerLifecycleEvent(
                        kernel_id,
                        known_kernels[kernel_id],
                        LifecycleEvent.CLEAN,
                        'self-terminated',
                    )
                for kernel_id, container in (await self.enumerate_containers(ACTIVE_STATUS_SET)):
                    alive_kernels[kernel_id] = container.id
                for kernel_id, kernel_obj in self.kernel_registry.items():
                    known_kernels[kernel_id] = kernel_obj['container_id']
                # Check if: kernel_registry has the container but it's gone.
                for kernel_id in (known_kernels.keys() - alive_kernels.keys()):
                    if kernel_id in self.terminating_kernels or kernel_id in self.restarting_kernels:
                        continue
                    terminated_kernels[kernel_id] = ContainerLifecycleEvent(
                        kernel_id,
                        known_kernels[kernel_id],
                        LifecycleEvent.CLEAN,
                        'self-terminated',
                    )
                # Check if: there are containers not spawned by me.
                for kernel_id in (alive_kernels.keys() - known_kernels.keys()):
                    if kernel_id in self.terminating_kernels or kernel_id in self.restarting_kernels:
                        continue
                    terminated_kernels[kernel_id] = ContainerLifecycleEvent(
                        kernel_id,
                        alive_kernels[kernel_id],
                        LifecycleEvent.DESTROY,
                        'terminated-unknown-container',
                    )
                # Check if: the container's idle timeout is expired.
                for kernel_id, kernel_obj in self.kernel_registry.items():
                    if kernel_id in self.terminating_kernels or kernel_id in self.restarting_kernels:
                        continue
                    idle_timeout = kernel_obj.resource_spec.idle_timeout
                    if idle_timeout is None or kernel_id not in alive_kernels:
                        continue
                    if idle_timeout > 0 and now - kernel_obj.last_used > idle_timeout:
                        terminated_kernels[kernel_id] = ContainerLifecycleEvent(
                            kernel_id,
                            kernel_obj['container_id'],
                            LifecycleEvent.DESTROY,
                            'idle-timeout',
                        )
            finally:
                # Enqueue the events.
                for kernel_id, ev in terminated_kernels.items():
                    self.container_lifecycle_queue.put_nowait(ev)

    async def clean_all_kernels(self, blocking: bool = False) -> None:
        kernel_ids = [*self.kernel_registry.keys()]
        clean_events = {}
        if blocking:
            for kernel_id in kernel_ids:
                clean_events[kernel_id] = asyncio.Event()
        for kernel_id in kernel_ids:
            await self.inject_container_lifecycle_event(
                kernel_id,
                LifecycleEvent.DESTROY,
                'agent-termination',
                clean_event=clean_events[kernel_id] if blocking else None,
            )
        if blocking:
            waiters = [clean_events[kernel_id].wait()
                       for kernel_id in kernel_ids]
            await asyncio.gather(*waiters)

    @abstractmethod
    async def detect_resources(self) -> Tuple[
        Mapping[DeviceName, AbstractComputePlugin],
        Mapping[SlotName, Decimal]
    ]:
        """
        Scan and define the amount of available resource slots in this node.
        """

    @abstractmethod
    async def scan_images(self) -> Mapping[str, str]:
        """
        Scan the available kernel images/templates and update ``self.images``.
        This is called periodically to keep the image list up-to-date and allow
        manual image addition and deletions by admins.
        """

    async def _scan_images_wrapper(self, interval: float) -> None:
        self.images = await self.scan_images()

    @abstractmethod
    async def pull_image(self, image_ref: ImageRef, registry_conf: ImageRegistry) -> None:
        '''
        Pull the given image from the given registry.
        '''

    @abstractmethod
    async def check_image(self, image_ref: ImageRef, image_id: str, auto_pull: AutoPullBehavior) -> bool:
        '''
        Check the availability of the image and return a boolean flag that indicates whether
        the agent should try pulling the image from a registry.
        '''
        return False

    async def scan_running_kernels(self) -> None:
        """
        Scan currently running kernels and recreate the kernel objects in
        ``self.kernel_registry`` if any missing.
        """
        try:
            with open(ipc_base_path / f'last_registry.{self.agent_id}.dat', 'rb') as f:
                self.kernel_registry = pickle.load(f)
                for kernel_obj in self.kernel_registry.values():
                    kernel_obj.agent_config = self.local_config
                    if kernel_obj.runner is not None:
                        await kernel_obj.runner.__ainit__()
        except FileNotFoundError:
            pass
        async with self.resource_lock:
            for kernel_id, container in (await self.enumerate_containers(
                ACTIVE_STATUS_SET | DEAD_STATUS_SET,
            )):
                if container.status in ACTIVE_STATUS_SET:
                    kernelspec = int(container.labels.get('ai.backend.kernelspec', '1'))
                    if not (MIN_KERNELSPEC <= kernelspec <= MAX_KERNELSPEC):
                        continue
                    # Consume the port pool.
                    for p in container.ports:
                        if p.host_port is not None:
                            self.port_pool.discard(p.host_port)
                    # Restore compute resources.
                    for computer_set in self.computers.values():
                        await computer_set.instance.restore_from_container(
                            container,
                            computer_set.alloc_map,
                        )
                    await self.inject_container_lifecycle_event(
                        kernel_id,
                        LifecycleEvent.START,
                        'resuming-agent-operation',
                        container_id=container.id,
                    )
                elif container.status in DEAD_STATUS_SET:
                    log.info('detected dead container while agent is down (k:{0}, c:{})',
                             kernel_id, container.id)
                    await self.inject_container_lifecycle_event(
                        kernel_id,
                        LifecycleEvent.CLEAN,
                        'self-terminated',
                        container_id=container.id,
                    )

        log.info('starting with resource allocations')
        for computer_name, computer_ctx in self.computers.items():
            log.info('{}: {!r}',
                     computer_name,
                     dict(computer_ctx.alloc_map.allocations))

    @abstractmethod
    async def create_kernel(
        self,
        creation_id: str,
        kernel_id: KernelId,
        config: KernelCreationConfig,
        *,
        restarting: bool = False,
    ) -> KernelCreationResult:
        """
        Create a new kernel.

        Things to do:
        * ``await self.produce_event('kernel_preparing', kernel_id)``
        * Check availability of kernel image using ``await self.check_image(...)``.
          - If it returns True:
          - ``await self.produce_event('kernel_pulling', kernel_id)``
          - Pull the kernel image using ``await self.pull_image(...)``.
        * ``await self.produce_event('kernel_creating', kernel_id)``
        * Create KernelResourceSpec object or read it from kernel's internal configuration cache.
          Use *restarting* argument to detect if the kernel is being created or restarted.
        * Determine the matched base-distro and kernel-runner volume name for the image
          using match_krunner_volume()
        * Set up the kernel-runner volume, other volumes, and bind-mounts.
        * Create and start the kernel (e.g., container, process, etc.) with statistics synchronizer.
        * Create the kernel object (derived from AbstractKernel) and add it to ``self.kernel_registry``.
        * ``await self.produce_event('kernel_started', kernel_id)``
        * Execute the startup command if the sessino type is batch.
        * Return the kernel creation result.
        """

        # TODO: clarify when to ``self.produce_event('kernel_terminated', ...)``

    @abstractmethod
    async def destroy_kernel(
        self,
        kernel_id: KernelId,
        container_id: Optional[ContainerId],
    ) -> None:
        """
        Initiate destruction of the kernel.

        Things to do:
        * Add the kernel ID to self.terminating_kernels if it's not in self.restarting_kernels
        * Send a forced-kill signal to the kernel
        """

    @abstractmethod
    async def clean_kernel(
        self,
        kernel_id: KernelId,
        container_id: Optional[ContainerId],
        restarting: bool,
    ) -> None:
        """
        Clean up kernel-related book-keepers when the underlying
        implementation detects an event that the kernel has terminated.

        Things to do:
        * Delete the underlying kernel resource (e.g., container)
        * Release host-specific resources used for the kernel (e.g., scratch spaces)
        * Discard the kernel ID from self.terminating_kernels if it's not in self.restarting_kernels

        This method is intended to be called asynchronously by the implementation-specific
        event monitoring routine.

        The ``container_id`` may be ``None`` if the container has already gone away.
        In such cases, skip container-specific cleanups.
        """

    async def restart_kernel(
        self,
        creation_id: str,
        kernel_id: KernelId,
        new_config: KernelCreationConfig,
    ):
        # TODO: check/correct resource release/allocation timings during restarts
        # TODO: handle restart failure when resource allocation for new config fails
        tracker = self.restarting_kernels.get(kernel_id)
        if tracker is None:
            tracker = RestartTracker(
                request_lock=asyncio.Lock(),
                destroy_event=asyncio.Event(),
                done_event=asyncio.Event())
            self.restarting_kernels[kernel_id] = tracker
        config_dir = (
            self.local_config['container']['scratch-root'] /
            str(kernel_id) /
            'config'
        ).resolve()
        with open(config_dir / 'kconfig.dat', 'rb') as fb:
            existing_config = pickle.load(fb)
            new_config = cast(KernelCreationConfig, {**existing_config, **new_config})
        async with tracker.request_lock:
            tracker.done_event.clear()
            await self.inject_container_lifecycle_event(
                kernel_id,
                LifecycleEvent.DESTROY,
                'restarting',
            )
            try:
                with timeout(60):
                    await tracker.destroy_event.wait()
            except asyncio.TimeoutError:
                log.warning('timeout detected while restarting kernel {0}!',
                            kernel_id)
                self.restarting_kernels.pop(kernel_id, None)
                await self.inject_container_lifecycle_event(
                    kernel_id,
                    LifecycleEvent.CLEAN,
                    'restart-timeout',
                )
                raise
            else:
                tracker.destroy_event.clear()
                await self.create_kernel(
                    creation_id,
                    kernel_id,
                    new_config,
                    restarting=True)
                self.restarting_kernels.pop(kernel_id, None)
            tracker.done_event.set()
        kernel_obj = self.kernel_registry[kernel_id]
        return {
            # TODO: generalize
            'container_id': kernel_obj['container_id'],
            'repl_in_port': kernel_obj['repl_in_port'],
            'repl_out_port': kernel_obj['repl_out_port'],
            'stdin_port': kernel_obj['stdin_port'],
            'stdout_port': kernel_obj['stdout_port'],
            'service_ports': kernel_obj.service_ports,
        }

    async def execute(self, kernel_id: KernelId,
                      run_id: Optional[str], mode: str, text: str, *,
                      opts: Mapping[str, Any],
                      api_version: int,
                      flush_timeout: float):
        # Wait for the kernel restarting if it's ongoing...
        restart_tracker = self.restarting_kernels.get(kernel_id)
        if restart_tracker is not None:
            await restart_tracker.done_event.wait()

        try:
            kernel_obj = self.kernel_registry[kernel_id]
            result = await kernel_obj.execute(
                run_id, mode, text,
                opts=opts,
                flush_timeout=flush_timeout,
                api_version=api_version)
        except KeyError:
            # This situation is handled in the lifecycle management subsystem.
            raise RuntimeError(f'The container for kernel {kernel_id} is not found! '
                                '(might be terminated--try it again)') from None

        if result['status'] in ('finished', 'exec-timeout'):
            log.debug('_execute({0}) {1}', kernel_id, result['status'])
        if result['status'] == 'exec-timeout':
            await self.inject_container_lifecycle_event(
                kernel_id,
                LifecycleEvent.DESTROY,
                'exec-timeout',
            )
        return {
            **result,
            'files': [],  # kept for API backward-compatibility
        }

    async def get_completions(self, kernel_id: KernelId, text: str, opts: dict):
        return await self.kernel_registry[kernel_id].get_completions(text, opts)

    async def get_logs(self, kernel_id: KernelId):
        return await self.kernel_registry[kernel_id].get_logs()

    async def interrupt_kernel(self, kernel_id: KernelId):
        return await self.kernel_registry[kernel_id].interrupt_kernel()

    async def start_service(self, kernel_id: KernelId, service: str, opts: dict):
        return await self.kernel_registry[kernel_id].start_service(service, opts)

    async def shutdown_service(self, kernel_id: KernelId, service: str):
        try:
            kernel_obj = self.kernel_registry[kernel_id]
            if kernel_obj is not None:
                await kernel_obj.shutdown_service(service)
        except Exception:
            log.exception('unhandled exception while shutting down service app ${}', service)

    async def accept_file(self, kernel_id: KernelId, filename: str, filedata):
        return await self.kernel_registry[kernel_id].accept_file(filename, filedata)

    async def download_file(self, kernel_id: KernelId, filepath: str):
        return await self.kernel_registry[kernel_id].download_file(filepath)

    async def list_files(self, kernel_id: KernelId, path: str):
        return await self.kernel_registry[kernel_id].list_files(path)
