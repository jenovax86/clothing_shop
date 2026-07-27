from http import HTTPStatus

class AbstractException(Exception):
    status_code: int = 500
    error_code: str = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundException(AbstractException):
    status_code: int = HTTPStatus.NOT_FOUND
    error_code: str = "Not Found"

class ConflictException(AbstractException):
    status_code: int = HTTPStatus.CONFLICT
    error_code: str = "Conflict"
