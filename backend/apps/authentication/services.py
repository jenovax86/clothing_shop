import os
import jwt
from datetime import datetime, timedelta, timezone
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from logging import getLogger

from apps.users.models import User
from core.exceptions import UserDidNotFound, PasswordDidNotMatch, TokenNotFound, TokenInvalid, TokenExpired

logger = getLogger(__name__)


class TokenService:

    @staticmethod
    def generate_access_token(user_id: int) -> str:
        logger.info(f"Generating token for user {user_id}")
        payload = {
            'user_id': user_id,
            'exp': datetime.now(timezone.utc) + timedelta(hours=5),
            'iat': datetime.now(timezone.utc)
        }
        logger.info(f"payload: {payload}")
        return jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')

    @staticmethod
    def verify_token(token: str) -> dict:
        print(jwt.exceptions.ExpiredSignatureError)
        print(jwt.exceptions.InvalidSignatureError)
        print(jwt.exceptions.InvalidTokenError)
        logger.info(f"Decode token {token}")
        if not token:
            logger.warning("Token not found")
            raise TokenNotFound("Token not found")
        try:
            valid_token: str = token.split(" ")[1]
            decoded_token: dict = jwt.decode(valid_token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
            return decoded_token
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            raise TokenInvalid("Invalid token")
        except jwt.ExpiredSignatureError:
            logger.warning("Expired token")
            raise TokenExpired("Expired token")


class AuthenticationService:
    @staticmethod
    def authenticate_user(username: str, password: str) -> User | None:
        logger.info(f"Authenticating user {username}")
        user = User.objects.filter(username=username).first()

        if user is None:
            logger.warning(f"User {username} not found")
            raise UserDidNotFound("User did not found")

        argon_hasher: PasswordHasher = PasswordHasher()
        try:
            argon_hasher.verify(user.password, password)
        except VerifyMismatchError:
            logger.warning(f"Password did not match")
            raise PasswordDidNotMatch("Password did not match")

        logger.info(f"User {username} authenticated")
        return user
