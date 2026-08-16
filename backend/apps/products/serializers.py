from rest_framework import serializers

from apps.products.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="name",
    )

    class Meta:
        model = Product
        fields = ["gender", "category", "name", "size", "price", "color"]

        category = serializers.CharField(max_length=30)
