import logging

from rest_framework.authentication import BaseAuthentication

from apps.authentication.services import TokenService
from apps.users.services import UserService
from core.exceptions import TokenNotFound, TokenInvalid, TokenExpired, UserDidNotFound

logger = logging.getLogger(__name__)


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        logger.info('Authenticating with JWT')
        token = request.headers.get("Authorization")
        if not token:
            raise TokenNotFound("Token not found")

        try:
            logger.info('Verifying JWT token')
            payload = TokenService.verify_token(token)
            user_id = payload.get("user_id")
            user = UserService.find_user_by_id(user_id)
            return user, token
        except TokenExpired:
            logger.info('Expired token')
            raise TokenExpired("Expired token")
        except TokenInvalid:
            logger.info('Invalid token')
            raise TokenInvalid("Invalid token")
        except UserDidNotFound:
            logger.info('User did not found')
            raise UserDidNotFound("UserDidNotFound")
