from rest_framework import serializers

from apps.products.models import Category, Product, ProductMedia


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["gender", "category", "name", "size", "price", "color"]


class ProductFilterSerializer(serializers.Serializer):
    gender = serializers.ChoiceField(choices=Product.Gender.choices, required=False)
    category = serializers.IntegerField(required=False, min_value=1)
    name = serializers.CharField(required=False)
    size = serializers.ChoiceField(choices=Product.Sizes.choices, required=False)
    price = serializers.FloatField(required=False)
    color = serializers.CharField(required=False)
    min_price = serializers.FloatField(required=False, min_value=0)
    max_price = serializers.FloatField(required=False, min_value=0)

class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ["id", "url"]
