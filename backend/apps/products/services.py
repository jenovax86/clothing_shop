import logging
from datetime import timezone, datetime

from apps.products.models import Product, Category
from core.exceptions import CategoryAlreadyExists, CategoryDoesNotExist, ProductAlreadyExists, ProductDoesNotExist

logger = logging.getLogger('django')


class CategoryService:
    @staticmethod
    def create_category(name: str) -> Category:
        logger.info(f"Creating category {name}")
        if Category.objects.filter(name=name).exists():
            logger.warning(f"Category {name} already exists")
            raise CategoryAlreadyExists("Category already exists.")

        return Category.objects.create(name=name)

    @staticmethod
    def list_categories() -> list[Category]:
        logger.info(f"Listing categories")
        categories = list(Category.objects.all())
        logger.info(f"Found {len(categories)} categories")
        return categories

    @staticmethod
    def get_category_by_id(category_id: int) -> Category:
        logger.info(f"Getting category by id {category_id}")
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            logger.warning(f"Category with id {category_id} does not exist")
            raise CategoryDoesNotExist("Category does not exist.")

    @staticmethod
    def get_category_by_name(name: str) -> Category:
        logger.info(f"Getting category by name {name}")
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            logger.warning(f"Category with name {name} does not exist")
            raise CategoryDoesNotExist("Category does not exist.")

    @staticmethod
    def update_category(category_id: int, name: str) -> None:
        logger.info(f"Changing category name {name}")
        try:
            category = CategoryService.get_category_by_id(category_id)
        except Category.DoesNotExist:
            logger.warning(f"Category with id {category_id} does not exist")
            raise CategoryDoesNotExist("Category does not exist.")
        category.name = name
        category.save()

    @staticmethod
    def delete_category(category_id: int) -> None:
        logger.info(f"Deleting category {category_id}")
        category = CategoryService.get_category_by_id(category_id)
        category.deleted_at = datetime.now(timezone.utc)
        category.save(update_fields=["deleted_at"])


class ProductService:
    @staticmethod
    def create_product(gender: str, category: Category, name: str, size: str, price: float, color: str) -> Product:
        logger.info(f"Creating product {name}")
        if Product.objects.filter(name=name).exists():
            logger.warning(f"Product with gender {name} already exists")
            raise ProductAlreadyExists("Product already exists.")

        return Product.objects.create(gender=gender, category=category, name=name, size=size, price=price,
                                      color=color)

    @staticmethod
    def get_products_by_gender(gender: str) -> list[Product]:
        logger.info(f"Getting products by gender {gender}")
        try:
            products = list(Product.objects.filter(gender=gender))
            return products
        except Product.DoesNotExist:
            logger.warning(f"Product with gender {gender} does not exist")
            raise ProductDoesNotExist("Product does not exist.")

    @staticmethod
    def get_product_by_id(product_id: int) -> Product:
        logger.info(f"Getting product by id {product_id}")
        try:
            product = Product.objects.get(id=product_id)
            return product
        except Product.DoesNotExist:
            logger.warning(f"Product with id {product_id} does not exist")
            raise ProductDoesNotExist("Product does not exist.")

    @staticmethod
    def update_product(product_id, product_fields: dict) -> Product:
        logger.info("Change product data")
        try:
            product = ProductService.get_product_by_id(product_id)
        except Product.DoesNotExist:
            logger.warning(f"Product with id {product_fields['id']} does not exist")
            raise ProductDoesNotExist("Product does not exist.")

        product.gender = product_fields['gender']
        product.name = product_fields['name']
        product.size = product_fields['size']
        product.price = product_fields['price']
        product.color = product_fields['color']
        product.save()

    @staticmethod
    def delete_product(product_id: int) -> None:
        logger.info(f"Deleting product {product_id}")
        product = ProductService.get_product_by_id(product_id)
        product.deleted_at = datetime.now(timezone.utc)
        product.save(update_fields=["deleted_at"])
