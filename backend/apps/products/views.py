import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import IsAdmin
from .models import Category
from .serializers import CategorySerializer, ProductSerializer
from .services import CategoryService, ProductService

logger = logging.getLogger(__name__)


class CreateCategory(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        logger.info("Post request")
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            CategoryService().create_category(serializer.validated_data["name"])
            logger.info("Category created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCategories(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        logger.info("get request")
        serializer = CategorySerializer(Category.objects.all(), many=True)
        logger.info("Listing categories")
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetCategory(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, category_id):
        logger.info("get request")
        serializer = CategorySerializer(CategoryService.get_category_by_id(category_id))
        logger.info("Category retrieved")
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateCategory(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, category_id):
        logger.info("patch request")
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            CategoryService.update_category(category_id, serializer.validated_data["name"])
            logger.info("Category updated successfully")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCategory(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, category_id):
        logger.info("delete request")
        CategoryService.delete_category(category_id)
        logger.info("Category deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateProduct(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            ProductService.create_product(serializer.validated_data["gender"], serializer.validated_data["category"],
                                          serializer.validated_data["name"], serializer.validated_data["size"],
                                          serializer.validated_data["price"], serializer.validated_data["color"], )
            logger.info(f"Product {serializer.validated_data['name']} is created.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetProduct(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, product_id):
        logger.info("get request")
        product = ProductService.get_product_by_id(product_id)
        serializer = ProductSerializer(product)
        logger.info("Product retrieved")
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProduct(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, product_id):
        logger.info("patch request")
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            ProductService.update_product(product_id, product_fields=serializer.validated_data)
            logger.info("Product updated successfully")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetProductByGender(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        logger.info("get request")
        gender = request.query_params.get("gender")
        product = ProductService.get_products_by_gender(gender)
        serializer = ProductSerializer(product, many=True)
        logger.info("Product retrieved")
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteProduct(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, product_id):
        logger.info("delete request")
        ProductService.delete_product(product_id)
        logger.info("Product deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)
