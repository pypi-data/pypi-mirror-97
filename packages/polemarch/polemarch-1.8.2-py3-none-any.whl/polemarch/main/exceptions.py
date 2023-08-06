from vstutils import exceptions


class PMException(exceptions.VSTUtilsException):
    pass


class UnknownTypeException(exceptions.UnknownTypeException):
    pass


class NodeFailedException(PMException):
    pass


class NodeOfflineException(PMException):
    pass


class AnsibleNotFoundException(PMException):
    pass


class DataNotReady(PMException):
    status = exceptions.status.HTTP_424_FAILED_DEPENDENCY


class NotApplicable(exceptions.NotApplicable):
    pass


class Conflict(PMException):
    status = exceptions.status.HTTP_409_CONFLICT
