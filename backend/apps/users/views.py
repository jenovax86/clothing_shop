import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import ChangeUsernameSerializer, ChangePasswordSerializer, AddressSerializer
from apps.users.services import UserService
from core.exceptions import PasswordIsIdentical

logger = logging.getLogger(__name__)


class ChangeUsername(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        logger.info(f"User requested")
        serializer = ChangeUsernameSerializer(data=request.data)
        if serializer.is_valid():
            UserService.change_username(request.user, serializer.validated_data["username"])
            logger.info(f"User {request.user} changed successfully")
            return Response({
                "success": True,
                "message": "User changed successfully",
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        logger.info(f"User password requested")
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]
            if old_password != new_password:
                UserService.change_password(request.user, serializer.validated_data["old_password"],
                                            serializer.validated_data["new_password"])
                logger.info(f"User {request.user} changed successfully")
                return Response({
                    "success": True,
                    "message": "Password changed successfully",
                })
            raise PasswordIsIdentical("Two passwords do match.")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateAddress(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info(f"Address requested")
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            UserService.add_user_address(user=request.user, address_data=serializer.validated_data)
            logger.info(f"Create {request.user.username} address")
            return Response({
                "success": True,
                "message": "Address created successfully",
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeAddress(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, address_id):
        logger.info(f"Address requested for changing")
        serializer = AddressSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            UserService.change_user_address(request.user, address_id, **serializer.validated_data)
            logger.info("Changed Address successfully")
            return Response({
                "success": True,
                "message": "Address changed successfully",
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAddress(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, address_id):
        logger.info(f"Address requested")
        UserService.delete_address(address_id)
        return Response({
            "success": True,
            "message": "Address deleted successfully",
        })
