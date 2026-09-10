import jwt
from datetime import datetime, timedelta, timezone
from django.contrib.auth.hashers import make_password, check_password
from apps.users.models import User
from .exceptions import TokenNotFound, InvalidToken, TokenExpired
from apps.users.exceptions import UserNotFound, IncorrectCredentials


class TokenService:
    def __init__(self, jwt_secret, logger):
        self.jwt_secret = jwt_secret
        self.logger = logger

    def generate_access_token(self, user_id: int) -> str:
        self.logger.info(f"Generating token for user {user_id}")
        payload = {
            'user_id': user_id,
            'exp': datetime.now(timezone.utc) + timedelta(hours=5),
            'iat': datetime.now(timezone.utc)
        }
        self.logger.info(f"payload: {payload}")

        return jwt.encode(
            payload,
            self.jwt_secret,
            algorithm='HS256'
        )

    def __decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.jwt_secret, algorithms=['hmac'])
        except jwt.ExpiredSignatureError:
            self.logger.warning("Expired token")
            raise TokenExpired("Expired token")
        except jwt.InvalidTokenError:
            self.logger.warning("Invalid token")
            raise InvalidToken("Invalid token exception")

    def verify_token(self, token: str) -> dict:
        self.logger.info(f"Decode token {token}")
        if not token:
            self.logger.warning("Token not found")
            raise TokenNotFound("Token not found")

        decoded_token: dict = self.__decode_token(token)
        return decoded_token


class AuthenticationService:
    def __init__(self, user_model, logger):
        self.user_model = user_model
        self.logger = logger

    def authenticate_user(self, username: str, password: str) -> User :
        self.logger.info(f"Authenticating user {username}")
        user = self.user_model.objects.get(username=username)

        if user is None:
            self.logger.warning(f"User {username} not found")
            raise UserNotFound("User not found")

        if not user.check_password(password):
            self.logger.warning(f"Username or password is wrong")
            raise IncorrectCredentials("Username or password is wrong exception")

        self.logger.info(f"User {username} authenticated")
        return user
