from rest_framework.permissions import BasePermission

from apps.users.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.role == "admin"
