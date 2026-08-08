from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/test_app/", include("apps.test_app.urls")),
    path("api/v1/auth/", include("apps.authentication.urls")),
    path("api/v1/", include("apps.users.urls")),
]
