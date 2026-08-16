from django.urls import path

from .views import CreateCategory, ListCategories, GetCategory, UpdateCategory, DeleteCategory, CreateProduct, \
    GetProduct, UpdateProduct, DeleteProduct, GetProductByGender

urlpatterns = [
    path('categories/create/', CreateCategory.as_view(), name='create-category'),
    path('categories/all/', ListCategories.as_view(), name='list-categories'),
    path('categories/get/<int:category_id>/', GetCategory.as_view(), name='get_category'),
    path('categories/update/<int:category_id>/', UpdateCategory.as_view(), name='update_category'),
    path('categories/delete/<int:category_id>/', DeleteCategory.as_view(), name='update_category'),
    path('products/create/', CreateProduct.as_view(), name='create_product'),
    path('products/get/<int:product_id>/', GetProduct.as_view(), name="get_product"),
    path('products/get/', GetProductByGender.as_view(), name="get_products_by_gender"),
    path('products/update/<int:product_id>/', UpdateProduct.as_view(), name="update_product"),
    path('products/delete/<int:product_id>/', DeleteProduct.as_view(), name="delete_product"),
]
