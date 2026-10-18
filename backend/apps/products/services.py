from datetime import timezone, datetime

from apps.products.models import Product, Category, ProductMedia
from .exceptions import CategoryAlreadyExists, CategoryNotFound


class CategoryService:
    def __init__(self, category_model, logger):
        self.category_model = category_model
        self.logger = logger

    def create_category(self, name: str) -> Category:
        self.logger.info(f"Creating category {name}")
        category, was_created = self.category_model.objects.get_or_create(name=name)
        if not was_created:
            self.logger.warning(f"Category {name} already exists")
            raise CategoryAlreadyExists("Category already exists exception.")

        return category

    def list_categories(self) -> list[Category]:
        self.logger.info(f"Listing categories")
        return list(self.category_model.objects.filter(deleted_at__isnull=True).order_by("name"))

    def get_category_by_id(self, category_id: int) -> Category:
        self.logger.info(f"Getting category by id {category_id}")
        try:
            return self.category_model.objects.get(id=category_id)
        except self.category_model.DoesNotExist:
            self.logger.warning(f"Category with id {category_id} does not exist")
            raise CategoryNotFound("Category does not exist exception.")

    def update_category(self, category_id: int, name: str) -> None:
        self.logger.info(f"Changing category name {name}")
        self.category_model.filter(pk=category_id, deleted_at__isnull=True).update(name=name)

    def delete_category(self, category_id: int) -> None:
        self.logger.info(f"Deleting category {category_id}")
        self.category_model.objects.filter(pk=category_id, deleted_at__isnull=True).update(
            deleted_at=datetime.now(timezone.utc))


class ProductService:
    def __init__(self, product_model, logger):
        self.product_model = product_model
        self.logger = logger

    def create_product(self, product_fields: dict) -> Product:
        self.logger.info(f"Creating product %s", product_fields["name"])
        product = self.product_model.objects.create(**product_fields)

        return product

    def list_products(self) -> list[Product]:
        self.logger.info(f"Listing products")
        return list(self.product_model.objects.filter(deleted_at__isnull=True).order_by("name"))

    def filter_product(self, filters: dict) -> Product:
        self.logger.info(f"Filtering product %s", filters)
        products = self.product_model.objects.filter(deleted_at__isnull=True)

        for field in ("gender", "name", "size", "price", "color", "category"):
            if field in filters:
                products = products.filter(**{field: filters[field]})

        if "min_price" in filters:
            products = products.filter(price__gte=filters["min_price"])

        if "max_price" in filters:
            products = products.filter(price__lte=filters["max_price"])

        return products.order_by("name")

    def update_product(self, product_id, product_fields: dict) -> None:
        self.logger.info("Change product fields")
        self.product_model.objects.filter(pk=product_id).update(**product_fields)

    def delete_product(self, product_id: int) -> None:
        self.logger.info(f"Deleting product {product_id}")
        self.product_model.objects.filter(pk=product_id, deleted_at__isnull=True).update(
            deleted_at=datetime.now(timezone.utc))


class ProductMediaService:
    def __init__(self, product_media_model, logger):
        self.product_media_model = product_media_model
        self.logger = logger

    def create_media(self, product_id: int, url: str) -> ProductMedia:
        self.logger.info(f"Creating product media %s", url)
        return self.product_media_model.objects.create(product_id=product_id, url=url)

    def list_all_medias(self, product_id: int) -> list[ProductMedia]:
        self.logger.info(f"Listing all medias for product %s", product_id)
        return list(self.product_media_model.objects.filter(product_id=product_id).order_by("url"))

    def update_product_media(self, product_id: int, media_id: int, new_url: str) -> None:
        self.logger.info(f"Changing product media url {new_url}")
        self.product_media_model.objects.filter(pk=media_id, product_id=product_id).update(url=new_url)

    def delete_product_media(self, product_id: int, media_id: int) -> None:
        self.logger.info(f"Deleting product media {product_id}")
        self.product_media_model.objects.filter(pk=media_id, product_id=product_id, deleted_at__isnull=True).delete()