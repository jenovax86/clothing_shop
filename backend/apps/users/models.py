from django.db import models


class Role(models.TextChoices):
    ADMIN = ("admin", "Admin")
    USER = ("user", "User")


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=20, null=False, blank=False)
    zip_code = models.CharField(max_length=20, null=False, blank=False)
    city = models.CharField(max_length=10, null=False, blank=False)
    province = models.CharField(max_length=20, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
