from rest_framework import serializers
import logging

from apps.users.models import User

logger = logging.getLogger(__name__)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    username = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)

    def validate_username(self, value: str) -> str:
        if User.objects.filter(username=value).exists():
            logger.info(f"User {value} already exists")
            raise serializers.ValidationError("Username already registered")

        return value


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    username = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)
