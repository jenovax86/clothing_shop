from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadingOnly(BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == "admin"
