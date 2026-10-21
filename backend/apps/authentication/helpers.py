import os
import logging

from .services import TokenService, AuthenticationService
from ..users.models import User


def get_token_service() -> TokenService:
    return TokenService(jwt_secret=os.getenv("JWT_TOKEN_SECRET"), logger=logging.getLogger(__name__), )


def get_auth_service() -> AuthenticationService:
    return AuthenticationService(user_model=User, logger=logging.getLogger(__name__), )
