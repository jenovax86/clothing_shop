from http import HTTPStatus

from core.exceptions import AbstractException


class UserDidNotFound(AbstractException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "Not Found"


class PasswordDidNotMatch(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Passwords don't match"


class MissingCredentials(AbstractException):
    status_code = HTTPStatus.CONFLICT
