from rest_framework import serializers
import logging

from .exceptions import UsernameIsRequired, PasswordIsRequired, IncorrectCredentials, AddressCantBeEmpty
from apps.users.models import User, Address

logger = logging.getLogger(__name__)


class ChangeUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

    def validate_username(self, value: str) -> str:
        if not value:
            logger.warning("Username cannot be None")
            raise UsernameIsRequired("Username is required")

        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')

        if not old_password or not new_password:
            logger.warning("Password cannot be None")
            raise PasswordIsRequired("Password is required")

        if old_password == new_password:
            logger.warning("Password is same")
            raise IncorrectCredentials("New password cannot match the old password.")
        return attrs


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('country', 'zip_code', 'city', 'province',)

    def validate(self, attrs):
        country = attrs.get('country')
        zip_code = attrs.get('zip_code')
        city = attrs.get('city')
        province = attrs.get('province')
        if not all((country, zip_code, city, province)):
            logger.warning("Address cannot be None")
            raise AddressCantBeEmpty("Address cannot be None")
        return attrs
