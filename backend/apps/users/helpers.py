import logging

from .models import User, Address
from .services import UserService


def get_user_service() -> UserService:
    return UserService(user_model=User, address_model=Address, logger=logging.getLogger(__name__))
