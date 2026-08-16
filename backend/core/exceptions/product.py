from http import HTTPStatus

from core.exceptions import AbstractException


class ProductAlreadyExists(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Product already exists"


class ProductDoesNotExist(AbstractException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "Product does not exist"
