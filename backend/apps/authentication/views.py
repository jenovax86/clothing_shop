import logging
import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.authentication.services import TokenService, AuthenticationService
from .serializers import RegisterSerializer, LoginSerializer
from apps.users.services import UserService
from ..users.models import Address, User

logger = logging.getLogger(__name__)


@api_view(['POST'])
def register_view(request):
    logger.info(f"Register request")
    serializer = RegisterSerializer(data=request.data)
    user_service = UserService(user_model=User, address_model=Address, logger=logger)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user_service.create_user(serializer.validated_data['username'], serializer.validated_data['password'])
    return Response({
        "success": True,
        "message": "User created successfully",
    }, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def login_view(request):
    logger.info(f"Login request")
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, )
    auth_service = AuthenticationService(user_model=User, logger=logger, )
    token_service = TokenService(jwt_secret=os.getenv("JWT_TOKEN_SECRET"), logger=logger, )

    user = auth_service.authenticate_user(serializer.validated_data["username"],
                                          serializer.validated_data["password"], )
    access_token = token_service.generate_access_token(user.id)
    logger.info(f"User {user.username} authenticated.")
    return Response({"success": True, "message": "User authenticated successfully", "token": access_token, },
                    status=status.HTTP_200_OK, )
