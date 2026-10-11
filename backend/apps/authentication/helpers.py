import os
import logging

from .services import TokenService


def get_token_service() -> TokenService:
    return TokenService(jwt_secret=os.getenv("JWT_TOKEN_SECRET"), logger=logging.getLogger(__name__), )
