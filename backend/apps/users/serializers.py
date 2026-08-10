from rest_framework import serializers
import logging

from apps.users.models import User, Address

logger = logging.getLogger(__name__)


class ChangeUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

    username = serializers.CharField(required=True)

    def validate_username(self, value: str) -> str:
        if User.objects.filter(username=value).exists():
            logger.warning(f"User {value} does exist")
            raise serializers.ValidationError("Username does exist")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('country', 'zip_code', 'city', 'province',)

    country = serializers.CharField(required=True)
    zip_code = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    province = serializers.CharField(required=True)
