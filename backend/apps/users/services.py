from datetime import datetime, timezone

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import logging

from core.exceptions import UsernameIsRequired, UserDidNotFound, PasswordDidNotMatch, user, AddressCantBeEmpty
from core.exceptions.user import UserAlreadyExists, PasswordIsRequired, AddressAlreadyExists, AddressDoesNotExist
from .models import User, Address

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def create_user(username: str, password: str) -> User:
        argon_hasher: PasswordHasher = PasswordHasher()
        hashed_password: str = argon_hasher.hash(password)
        user: User = User.objects.create(username=username, password=hashed_password)
        logger.info(f"User {username} created")
        return user

    @staticmethod
    def find_user_by_id(id: int) -> User:
        if not User.objects.filter(id=id).exists():
            logger.warning("User not found")
            raise UserDidNotFound(f"User {id} not found")
        return User.objects.get(id=id)

    @staticmethod
    def change_username(old_username: str, new_username: str) -> None:
        if not old_username or not new_username:
            logger.warning("Username cannot be None")
            raise UsernameIsRequired("Username is required")

        if User.objects.filter(username=new_username).exists():
            logger.warning("Username already exists")
            raise UserAlreadyExists("Username already exists")
        try:
            user: User = User.objects.get(username=old_username)
        except User.DoesNotExist:
            logger.warning("Username does not exist")
            raise UserDidNotFound("Username not found")

        user.username = new_username
        user.save(update_fields=["username"])

    @staticmethod
    def change_password(user: User, old_password: str, new_password: str) -> None:
        if not old_password or not new_password:
            logger.warning("Password cannot be None")
            raise PasswordIsRequired("Password is required")

        password_hasher: PasswordHasher = PasswordHasher()
        try:
            logger.info("Verifying password")
            password_hasher.verify(user.password, old_password)
        except VerifyMismatchError:
            logger.warning("Password does not match")
            raise PasswordDidNotMatch("Password does not match")
        hashed_password: str = password_hasher.hash(new_password)
        user.password = hashed_password
        user.save(update_fields=["password"])

    @staticmethod
    def add_user_address(**address) -> None:
        if not address:
            logger.warning("Address cannot be None")
            raise AddressCantBeEmpty("Address cannot be empty.")

        if Address.objects.filter(**address).exists():
            raise AddressAlreadyExists("Address already exists")

        Address.objects.create(**address)

    @staticmethod
    def change_user_address(user: User, address_id: int, **address_fields) -> None:
        old_address = Address.objects.filter(user_id=user.id, id=address_id).first()
        if old_address is None:
            logger.warning("Address does not exist")
            raise AddressDoesNotExist("Address does not exist")

        old_address.country = address_fields["country"]
        old_address.city = address_fields["city"]
        old_address.zip_code = address_fields["zip_code"]
        old_address.save()

    @staticmethod
    def delete_address(id: int) -> None:
        if not Address.objects.filter(id=id).exists():
            logger.warning("Address does not exist")
            raise AddressDoesNotExist("Address does not exist")
        address = Address.objects.get(id=id)
        address.deleted_at = datetime.now(timezone.utc)
        address.save(update_fields=["deleted_at"])
