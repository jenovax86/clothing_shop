from django.db import models


class Categories(models.Model):
    class Category(models.TextChoices):
        T_SHIRTS = "t_shirts", "T-Shirts"
        SHIRTS = "shirts", "Shirts"
        HOODIES = "hoodies", "Hoodies"
        SWEATSHIRTS = "sweatshirts", "Sweatshirts"
        SWEATERS = "sweaters", "Sweaters"
        JACKETS = "jackets", "Jackets"
        COATS = "coats", "Coats"
        JEANS = "jeans", "Jeans"
        TROUSERS = "trousers", "Trousers"
        SHORTS = "shorts", "Shorts"
        DRESSES = "dresses", "Dresses"
        SKIRTS = "skirts", "Skirts"
        ACTIVEWEAR = "activewear", "Activewear"
        UNDERWEAR = "underwear", "Underwear"
        SWIMWEAR = "swimwear", "Swimwear"
        SHOES = "shoes", "Shoes"
        ACCESSORIES = "accessories", "Accessories"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, choices=Category.choices, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Products(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    class Sizes(models.TextChoices):
        SMALL = "small", "Small"
        MEDIUM = "medium", "Medium"
        LARGE = "large", "Large"
        X_LARGE = "XL", "XL"
        XX_LARGE = "XXL", "XXL"
        XXX_LARGE = "XXXL", "XXXL"
        XXXX_LARGE = "XXXXL", "XXXXL"

    class Colors(models.TextChoices):
        RED = "red", "Red"
        GREEN = "green", "Green"
        BLUE = "blue", "Blue"
        YELLOW = "yellow", "Yellow"
        WHITE = "white", "White"
        BLACK = "black", "Black"
        GRAY = "gray", "Gray"
        BROWN = "brown", "Brown"
        PURPLE = "purple", "Purple"
        ORANGE = "orange", "Orange"
        PINK = "pink", "Pink"
        BEIGE = "beige", "Beige"
        NAVY = "navy", "Navy"
        OLIVE = "olive", "Olive"

    id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    size = models.CharField(max_length=15, choices=Sizes.choices, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    color = models.CharField(max_length=15, choices=Colors.choices, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
