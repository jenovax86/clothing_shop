from django.urls import path

from . import views

urlpatterns = [
    path("users/username/", views.change_username, name="change_username"),
    path("users/password/", views.change_password, name="change_password"),
    path("addresses/", views.create_address, name="create_address"),
    path("addresses/<int:address_id>/", views.address_detail, name="address_detail"),
]
