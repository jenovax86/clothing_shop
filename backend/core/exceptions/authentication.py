from http import HTTPStatus

from core.exceptions import AbstractException


class AuthenticationFailed(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Authentication failed"

