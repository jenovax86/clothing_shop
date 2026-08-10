from django.urls import path

from .views import ChangeUsername, ChangePassword, CreateAddress, ChangeAddress, DeleteAddress

urlpatterns = [
    path("user/change_username/", ChangeUsername.as_view(), name="change_username"),
    path("user/change_password/", ChangePassword.as_view(), name="change_password"),
    path("addresses/create/", CreateAddress.as_view(), name="create_address"),
    path("addresses/edit/<int:address_id>/", ChangeAddress.as_view(), name="edit_address"),
    path("addresses/delete/<int:address_id>/", DeleteAddress.as_view(), name="delete_address"),
]
