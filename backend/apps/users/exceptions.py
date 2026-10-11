from http import HTTPStatus

from core.exceptions import AbstractException


class UserNotFound(AbstractException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "Not found"


class MissingCredentials(AbstractException):
    status_code = HTTPStatus.BAD_REQUEST
    error_code = "Missing credentials"


class IncorrectCredentials(AbstractException):
    status_code = HTTPStatus.UNAUTHORIZED
    error_code = "Incorrect credentials"


class PasswordUnchanged(AbstractException):
    status_code = HTTPStatus.BAD_REQUEST
    error_code = "Password unchanged"

class UsernameIsRequired(AbstractException):
    status_code = HTTPStatus.BAD_REQUEST
    error_code = "Username not found"


class PasswordIsRequired(AbstractException):
    status_code = HTTPStatus.BAD_REQUEST
    error_code = "Password is required"


class AddressCantBeEmpty(AbstractException):
    status_code = HTTPStatus.BAD_REQUEST
    error_code = "Address can't be empty"


class AddressAlreadyExists(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Address already exists"


class AddressNoFound(AbstractException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "Address not found"
