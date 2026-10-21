import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .helpers import get_token_service, get_auth_service
from .serializers import RegisterSerializer, LoginSerializer
from ..users.helpers import get_user_service

logger = logging.getLogger(__name__)

token_service = get_token_service()
user_service = get_user_service()
auth_service = get_auth_service()


@api_view(['POST'])
def register_view(request):
    logger.info("Register request")
    serializer = RegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user_service.create_user(serializer.validated_data['username'], serializer.validated_data['password'])
    return Response({
        "success": True,
        "message": "User created successfully",
    }, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def login_view(request):
    logger.info("Login request")
    cookie_time_limit = 5 * 60 * 60
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, )

    user = auth_service.authenticate_user(serializer.validated_data["username"],
                                          serializer.validated_data["password"], )
    access_token = token_service.generate_access_token(user.id)
    refresh_token = token_service.generate_refresh_token(user.id)
    logger.info(f"User {user.username} authenticated.")

    response = Response({"success": True, "message": "User authenticated successfully", "token": access_token, },
                        status=status.HTTP_200_OK, )

    response.set_cookie(key="refresh", value=refresh_token, max_age=cookie_time_limit, httponly=True)
    return response


@api_view(["GET"])
def refresh_view(request):
    logger.info("Refresh request")
    refresh_token = request.COOKIES.get("refresh")

    if not refresh_token:
        logger.warning("No refresh token")
        return Response({"success": False, "message": "There is no refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

    payload = token_service.verify_token(refresh_token)
    user = user_service.find_user_by_id(payload['user_id'])
    access_token = token_service.generate_access_token(user.id)
    logger.info("New access token generated")
    return Response({"success": True, "message": "New token generated successfully", "token": access_token, },
                    status=status.HTTP_200_OK)
