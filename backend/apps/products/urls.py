from django.urls import path

from . import views

urlpatterns = [
    path('categories/', views.category_list_create, name='category_list_create'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('products/', views.product_list_create, name='product_list_create'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/filter/', views.filter_product, name="get_product"),
    path('product_media/<int:product_id>/', views.product_media_list_create, name='product_media_list_create'),
    path('product_media/<int:product_id>/<int:media_id>/', views.product_media_detail, name='product_media_detail'),

]
