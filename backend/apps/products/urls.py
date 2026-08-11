from django.urls import path

from .views import CreateCategory

urlpatterns = [
    path('categories/create', CreateCategory.as_view(), name='create-category'),
]
