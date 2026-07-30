from typing import Any
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from core.exceptions import AbstractException


def api_exception_handler(exception: Exception, context: dict[str, Any]) -> Response:
    response = drf_exception_handler(exception, context)

    if response is not None:
        return response

    if isinstance(exception, AbstractException):
        return Response(
            {
                "success": False,
                "message": exception.error_code,
            },
            status=exception.status_code,
        )
    return Response(
        {
            "success": False,
            "message": "Internal server error",

        },
        status=500,
    )
