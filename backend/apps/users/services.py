from datetime import datetime, timezone

from django.contrib.auth.hashers import make_password

from .models import User, Address
from .exceptions import UserNotFound, IncorrectCredentials, PasswordUnchanged
from apps.users.exceptions import AddressAlreadyExists, AddressNoFound


class UserService:
    def __init__(self, user_model: User, address_model: Address, logger):
        self.user_model = user_model
        self.address_model = address_model
        self.logger = logger

    def create_user(self, username: str, password: str) -> User:
        hashed_password: str = make_password(password)
        user = self.user_model.objects.create(username=username, password=hashed_password)
        self.logger.info(f"User {username} created")
        return user

    def find_user_by_id(self, user_id: int) -> User:
        try:
            return self.user_model.objects.get(id=user_id)
        except self.user_model.DoesNotExist:
            self.logger.warning("User not found")
            raise UserNotFound(f"User {id} not found exception.")

    def change_username(self, user: User, new_username: str) -> None:
        user.username = new_username
        user.save(update_fields=["username"])

    def change_password(self, user: User, old_password: str, new_password: str) -> None:
        if not user.check_password(old_password):
            self.logger.warning("Old password is incorrect.")
            raise IncorrectCredentials("Old password is incorrect exception.")

        if old_password == new_password:
            self.logger.warning("Password unchanged.")
            raise PasswordUnchanged("New password needs to be different than old password exception.")

        user.set_password(new_password)
        user.save(update_fields=["password"])

    def add_user_address(self, user: User, address_fields: dict) -> Address:
        if self.address_model.objects.filter(user=user, deleted_at__isnull=True, **address_fields).exists():
            self.logger.warning("Address already exists")
            raise AddressAlreadyExists("Address already exists exception.")

        return self.address_model.objects.create(user=user, **address_fields)

    def change_user_address(self, user: User, address_id: int, address_fields: dict) -> None:
        self.address_model.objects.filter(user_id=user, id=address_id).update(**address_fields)

    def delete_user_address(self, user: User, address_id: int) -> None:
        self.address_model.objects.filter(pk=address_id, user_id=user, deleted_at__isnull=True).update(
            deleted_at=datetime.now(timezone.utc))
