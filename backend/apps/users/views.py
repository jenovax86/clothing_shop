import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.services import TokenService
from apps.users.serializers import ChangeUsernameSerializer, ChangePasswordSerializer, AddressSerializer
from apps.users.services import UserService
from core.exceptions import PasswordIsIdentical

logger = logging.getLogger(__name__)


class ChangeUsername(APIView):
    def patch(self, request):
        logger.info(f"User requested")
        decoded_token = TokenService.decode_token(request.headers.get("Authorization").split(" ")[1])
        user = UserService.find_user_by_id(decoded_token.get("user_id")).username
        serializer = ChangeUsernameSerializer(data=request.data)

        if serializer.is_valid():
            UserService.change_username(user, serializer.validated_data["username"])
            logger.info(f"User {user} changed successfully")
            return Response({
                "success": True,
                "message": "User changed successfully",
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    def patch(self, request):
        logger.info(f"User password requested")
        decoded_token = TokenService.decode_token(request.headers.get("Authorization").split(" ")[1])
        user = UserService.find_user_by_id(decoded_token.get("user_id"))
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]
            if old_password != new_password:
                UserService.change_password(user, serializer.validated_data["old_password"],
                                            serializer.validated_data["new_password"])
                logger.info(f"User {user} changed successfully")
                return Response({
                    "success": True,
                    "message": "Password changed successfully",
                })
            raise PasswordIsIdentical("Two passwords do match.")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateAddress(APIView):
    def post(self, request):
        logger.info(f"Address requested")
        decoded_token = TokenService.decode_token(request.headers.get("Authorization").split(" ")[1])
        user = UserService.find_user_by_id(decoded_token.get("user_id"))
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            UserService.add_user_address(user=user, country=serializer.validated_data["country"],
                                         zip_code=serializer.validated_data["zip_code"],
                                         city=serializer.validated_data["city"],
                                         province=serializer.validated_data["province"])
            logger.info(f"Create {user.username} address")
            return Response({
                "success": True,
                "message": "Address created successfully",
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeAddress(APIView):
    def patch(self, request, address_id):
        logger.info(f"Address requested for changing")
        decoded_token = TokenService.decode_token(request.headers.get("Authorization").split(" ")[1])
        user = UserService.find_user_by_id(decoded_token.get("user_id"))
        serializer = AddressSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            UserService.change_user_address(user, address_id, **serializer.validated_data)
            logger.info("Changed Address successfully")
            return Response({
                "success": True,
                "message": "Address changed successfully",
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAddress(APIView):
    def patch(self, request, address_id):
        logger.info(f"Address requested")
        UserService.delete_address(address_id)
        return Response({
            "success": True,
            "message": "Address deleted successfully",
        })
