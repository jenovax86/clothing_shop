import logging
from typing import Any
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response

from core.exceptions import AbstractException

logger = logging.getLogger(__name__)


def api_exception_handler(exception: Exception, context: dict[str, Any]) -> Response:
    logger.exception(exception)
    response = drf_exception_handler(exception, context)

    if isinstance(exception, AbstractException):
        return Response(
            {
                "success": False,
                "error_code": exception.error_code,
                "message": exception.message,
            },
            status=exception.status_code,
        )

    if response is not None:
        return Response({
            "success": False,
            "message": response.data,
        },
            status=response.status_code,
        )

    return Response(
        {
            "success": False,
            "message": "Internal server error",

        },
        status=500,
    )
