import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)

from apps.users.serializers import ChangeUsernameSerializer, ChangePasswordSerializer, AddressSerializer
from .helpers import get_user_service
from ..authentication.authentication import JWTAuthentication

logger = logging.getLogger(__name__)
user_service = get_user_service()


@api_view(['Patch'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def change_username(request):
    logger.info(f"Update username request")
    serializer = ChangeUsernameSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user_service.change_username(request.user, serializer.validated_data['username'])
    return Response({
        "success": True,
        "message": "Username changed successfully"
    }, status=status.HTTP_200_OK)


@api_view(['Patch'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def change_password(request):
    logger.info(f"Update password request")
    serializer = ChangePasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    old_password = serializer.validated_data['old_password']
    new_password = serializer.validated_data['new_password']
    user_service.change_password(request.user, old_password, new_password)
    return Response({"success": True, "message": "Password changed successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_address(request):
    logger.info(f"Create address request")
    serializer = AddressSerializer(data=request.data)
    print("thisi si user:", request.user)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user_service.add_user_address(user=request.user, address_fields=serializer.validated_data)
    return Response({
        "success": True,
        "message": "Address created successfully"
    }, status=status.HTTP_201_CREATED)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def address_detail(request, address_id):
    logger.info(f"Address detail request")

    if request.method == "PATCH":
        serializer = AddressSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_service.change_user_address(request.user, address_id=address_id,
                                               address_fields=serializer.validated_data)
        return Response({
            "success": True,
            "message": "Address updated successfully"
        }, status=status.HTTP_200_OK)

    user_service.delete_user_address(request.user, address_id=address_id)
    return Response({
        "success": True,
        "message": "Address deleted successfully"
    }, status=status.HTTP_204_NO_CONTENT)


