class InitializationError(Exception):
    pass


class ResourceError(ValueError):
    pass


class UnsupportedResource(ResourceError):
    pass


class InvalidResourceCombination(ResourceError):
    pass


class InvalidResourceArgument(ResourceError):
    pass


class InsufficientResource(ResourceError):
    pass


class K8sError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
