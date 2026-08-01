from argon2 import PasswordHasher
import logging

from .models import User

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def create_user(username: str, password: str) -> User:
        argon_hasher: PasswordHasher = PasswordHasher()
        hashed_password = argon_hasher.hash(password)
        user = User.objects.create(username=username, password=hashed_password)
        logger.info(f"User {username} created")
        return user
