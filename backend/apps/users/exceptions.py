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
    error_code = "Missing Credentials"


class UsernameIsRequired(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Username not found"


class UserAlreadyExists(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Username already exists"


class PasswordIsRequired(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Password is required"


class PasswordIsIdentical(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Password is same"


class AddressCantBeEmpty(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Address can't be empty"


class AddressAlreadyExists(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Address already exists"

class AddressDoesNotExist(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Address does not exist"