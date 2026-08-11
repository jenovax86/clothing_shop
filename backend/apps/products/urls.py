from django.urls import path

from .views import CreateCategory, ListCategories, GetCategory, UpdateCategory, DeleteCategory

urlpatterns = [
    path('categories/create/', CreateCategory.as_view(), name='create-category'),
    path('categories/all/', ListCategories.as_view(), name='list-categories'),
    path('categories/get/<int:category_id>/', GetCategory.as_view(), name='get-category'),
    path('categories/update/<int:category_id>/', UpdateCategory.as_view(), name='update_category'),
    path('categories/delete/<int:category_id>/', DeleteCategory.as_view(), name='update_category'),
]
