import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.services import TokenService, AuthenticationService
from .serializers import RegisterSerializer, LoginSerializer
from apps.users.services import UserService

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    def post(self, request):
        logger.info(f"Post request: {request.data}")
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = UserService.create_user(serializer.validated_data['username'], serializer.validated_data['password'])
            logger.info(f"User {user.username} created")
            return Response({
                "success": True,
                "message": "User created successfully",
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        logger.info(f"Post request: {request.data}")
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            logger.info("Serializer validated")

            user = AuthenticationService.authenticate_user(serializer.validated_data['username'],
                                                           serializer.validated_data['password'])
            logger.info(f"User {user.username} authenticated")
            access_token = TokenService.generate_access_token(user.id)
            return Response({
                "success": True,
                "token": access_token,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
