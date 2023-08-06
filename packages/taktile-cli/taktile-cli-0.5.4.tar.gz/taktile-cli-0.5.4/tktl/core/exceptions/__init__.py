class ApplicationError(Exception):
    ...


class TaktileSdkError(Exception):
    ...


class AuthenticationError(ApplicationError):
    ...


class ArchiveUploadError(TaktileSdkError):
    ...


class PresignedUrlAccessDeniedError(ArchiveUploadError):
    ...


class ResourceFetchingError(TaktileSdkError):
    ...


class ResourceCreatingError(TaktileSdkError):
    ...


class MalformedResponseError(TaktileSdkError):
    ...


class ResourceCreatingDataError(ResourceCreatingError):
    ...


class PresignedUrlMalformedResponseError(ArchiveUploadError):
    ...


class PresignedUrlError(ArchiveUploadError):
    ...


class ProjectAccessDeniedError(ArchiveUploadError):
    ...


class WrongPathError(ArchiveUploadError):
    ...


class PresignedUrlUnreachableError(ArchiveUploadError):
    ...


class PresignedUrlConnectionError(ArchiveUploadError):
    ...


class InvalidParametersError(TaktileSdkError):
    ...


class BadResponseError(ApplicationError):
    ...


class InvalidInputError(ApplicationError):
    ...


class MutuallyExclusiveParametersUsedError(Exception):
    ...


class SerializerException(Exception):
    ...


class UnsupportedInputTypeException(Exception):
    ...
