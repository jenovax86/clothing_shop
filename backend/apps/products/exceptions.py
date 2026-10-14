from http import HTTPStatus

from core.exceptions import AbstractException


class ProductAlreadyExists(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Product already exists"


class ProductNotFound(AbstractException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "Product not found"


class CategoryAlreadyExists(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Category already exists"


class CategoryNotFound(AbstractException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "Category not found"
