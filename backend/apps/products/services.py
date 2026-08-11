import logging
from datetime import timezone, datetime

from apps.products.models import Product, Category
from core.exceptions import CategoryAlreadyExists, CategoryDoesNotExist

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
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            logger.warning(f"Category with id {category_id} does not exist")
            raise CategoryDoesNotExist("Category does not exist.")
        return category

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
        category.delete()
        category.deleted_at = datetime.now(timezone.utc)


class ProductService:
    @staticmethod
    def create_product(gender: str, name: str, size: str, price: float, color: str) -> None:
        ...

    @staticmethod
    def get_product_by_name(name: str):
        ...

    @staticmethod
    def get_products_by_gender(gender: str) -> list[Product]:
        ...

    @staticmethod
    def get_product_by_id(product_id: int) -> Product:
        ...

    @staticmethod
    def update_product_field(product: Product) -> Product:
        ...

    @staticmethod
    def delete_product(product_id: int) -> None:
        ...
