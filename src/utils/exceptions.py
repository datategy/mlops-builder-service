from httpx import HTTPStatusError


class MaxRetryErrors(BaseExceptionGroup):
    def __init__(self, message: str, excs: list[HTTPStatusError]):
        super().__init__(message, excs)


class FilesNotFound(BaseExceptionGroup):
    def __init__(self, message: str, excs: list[FileNotFoundError]):
        super().__init__(message, excs)
