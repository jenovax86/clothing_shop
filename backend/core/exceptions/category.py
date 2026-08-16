from http import HTTPStatus

from core.exceptions import AbstractException


class CategoryAlreadyExists(AbstractException):
    status_code = HTTPStatus.CONFLICT
    error_code = "Category already exists"


class CategoryDoesNotExist(AbstractException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "Category does not exist"
