import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)

from core.permissions import IsAdminOrReadingOnly

from .serializers import CategorySerializer, ProductSerializer, ProductFilterSerializer, ProductMediaSerializer
from .helpers import (get_category_service, get_product_service, get_product_media_service)
from ..authentication.authentication import JWTAuthentication

logger = logging.getLogger(__name__)

category_service = get_category_service()
product_service = get_product_service()
product_media_service = get_product_media_service()


@api_view(['POST', "GET"])
@permission_classes([IsAuthenticated, IsAdminOrReadingOnly])
@authentication_classes([JWTAuthentication])
def category_list_create(request):
    logger.info("Create new category")
    if request.method == "GET":
        logger.info("Listing categories")
        categories = category_service.list_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response(
            {"success": True, "message": "Categories retrieved successfully", "categories": serializer.data},
            status=status.HTTP_200_OK)

    serializer = CategorySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    category_service.create_category(serializer.validated_data['name'])
    return Response({"success": True, "message": "Category created successfully"}, status=status.HTTP_201_CREATED)


@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminOrReadingOnly])
@authentication_classes([JWTAuthentication])
def category_detail(request, category_id):
    logger.info("update category")
    serializer = CategorySerializer(data=request.data)

    if request.method == "PATCH":
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        category_service.update_category(serializer.validated_data["name"])
        return Response({"success": True, "message": "Category updated successfully"},
                        status=status.HTTP_204_NO_CONTENT)

    category_service.delete_category(category_id=category_id)
    return Response({
        "success": True,
        "message": "category deleted successfully"
    }, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated, IsAdminOrReadingOnly])
@authentication_classes([JWTAuthentication])
def product_list_create(request):
    logger.info("Create new product")
    if request.method == "GET":
        logger.info("Listing products")
        products = product_service.list_products()
        serializer = ProductSerializer(products, many=True)
        return Response(
            {"success": True, "message": "Products retrieved successfully", "products": serializer.data},
            status=status.HTTP_200_OK)

    serializer = ProductSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    product_service.create_product(serializer.validated_data)
    return Response({"success": True, "message": "Product created successfully"})


@api_view(["GET"])
def filter_product(request):
    logger.info("Filter product")
    filters = ProductFilterSerializer(data=request.query_params)
    if not filters.is_valid():
        return Response(filters.errors, status=status.HTTP_400_BAD_REQUEST)
    filtered_products = product_service.filter_product(filters.validated_data)
    products = ProductSerializer(filtered_products, many=True)

    return Response({"success": True, "message": "Product filtered successfully", "products": products.data},
                    status=status.HTTP_200_OK)


@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminOrReadingOnly])
@authentication_classes([JWTAuthentication])
def product_detail(request, product_id):
    serializer = ProductSerializer(data=request.data)
    if request.method == "PATCH":
        logger.info("update product")
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        product_service.update_product(product_id=product_id, product_fields=serializer.validated_data)
        return Response({"success": True, "message": "Product updated successfully"}, status=status.HTTP_204_NO_CONTENT)

    product_service.delete_product(product_id=product_id)
    return Response({"success": True, "message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated, IsAdminOrReadingOnly])
@authentication_classes([JWTAuthentication])
def product_media_list_create(request, product_id):
    if request.method == "GET":
        logger.info("Listing product medias")
        product_medias = product_media_service.list_all_medias(product_id=product_id)
        serializer = ProductMediaSerializer(product_medias, many=True)
        return Response(
            {"success": True, "message": "Product medias retrieved successfully", "products": serializer.data},
            status=status.HTTP_200_OK)

    logger.info("Add new product media")
    serializer = ProductMediaSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    product_media_service.create_media(product_id=product_id, url=serializer.validated_data["url"])
    return Response({"success": True, "message": "Product media created successfully"}, status=status.HTTP_201_CREATED)


@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminOrReadingOnly])
@authentication_classes([JWTAuthentication])
def product_media_detail(request, product_id, media_id):
    serializer = ProductMediaSerializer(data=request.data)
    if request.method == "PATCH":
        logger.info("Update product media")
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_media_service.update_product_media(product_id=product_id, media_id=media_id,
                                                   new_url=serializer.validated_data["url"])

        return Response({"success": True, "message": "Product media updated successfully"}, status=status.HTTP_200_OK)
    logger.info("Delete product media")
    product_media_service.delete_product_media(product_id=product_id, media_id=media_id)
    return Response({"success": True, "message": "Product media deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT)
