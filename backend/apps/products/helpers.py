import logging

from .models import Category, Product, ProductMedia
from .services import ProductService, CategoryService, ProductMediaService


def get_category_service() -> CategoryService:
    return CategoryService(category_model=Category, logger=logging.getLogger(__name__))


def get_product_service() -> ProductService:
    return ProductService(product_model=Product, logger=logging.getLogger(__name__))


def get_product_media_service() -> ProductMediaService:
    return ProductMediaService(product_media_model=ProductMedia, logger=logging.getLogger(__name__))
