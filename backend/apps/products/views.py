from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category
from .serializers import CategorySerializer
from .services import CategoryService


class CreateCategory(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            CategoryService().create_category(serializer.validated_data["name"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCategories(APIView):
    def get(self, request):
        serializer = CategorySerializer(Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetCategory(APIView):
    def get(self, request, category_id):
        serializer = CategorySerializer(CategoryService.get_category_by_id(category_id))
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateCategory(APIView):
    def patch(self, request, category_id):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            CategoryService.update_category(category_id, serializer.validated_data["name"])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCategory(APIView):
    def delete(self, request, category_id):
        CategoryService.delete_category(category_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
