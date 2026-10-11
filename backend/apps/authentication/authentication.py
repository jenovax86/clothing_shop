import logging

from rest_framework.authentication import BaseAuthentication

from .exceptions import AuthenticationFailed
from .helpers import get_token_service
from ..users.helpers import get_user_service

logger = logging.getLogger(__name__)


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        logger.info('Authentication JWT token')
        token_header = request.headers.get('Authorization')
        if not token_header:
            return None

        try:
            scheme, token = token_header.split(" ", 1)
        except ValueError:
            logger.warning('Invalid authorization header.')
            raise AuthenticationFailed("Invalid authorization header exception")

        if scheme != "Bearer":
            logger.warning('Invalid authorization scheme.')
            raise AuthenticationFailed("Invalid authorization scheme exception")

        token_service = get_token_service()
        user_service = get_user_service()
        try:
            payload = token_service.verify_token(token)
            user = user_service.find_user_by_id(payload["user_id"])
        except AuthenticationFailed:
            logger.warning('Cannot verify token.')
            raise AuthenticationFailed("Cannot verify token exception.")

        return user, payload
