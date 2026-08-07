from http import HTTPStatus

from core.exceptions import AbstractException


class AuthenticationFailed(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Authentication failed"


class TokenExpired(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Token expired"


class TokenInvalid(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Token invalid"


class TokenNotFound(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Token not found"
