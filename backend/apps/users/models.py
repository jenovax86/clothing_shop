from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models.functions import Now


class Role(models.TextChoices):
    ADMIN = ("admin", "Admin")
    USER = ("user", "User")


class User(AbstractBaseUser):
    USERNAME_FIELD = "username"

    class Meta:
        db_table = "users"

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    created_at = models.DateTimeField(db_default=Now())
    updated_at = models.DateTimeField(db_default=Now())
    deleted_at = models.DateTimeField(null=True, blank=True)


class Address(models.Model):
    class Meta:
        db_table = "addresses"

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=20, null=False, blank=False)
    zip_code = models.CharField(max_length=20, null=False, blank=False)
    city = models.CharField(max_length=10, null=False, blank=False)
    province = models.CharField(max_length=20, null=False, blank=False)
    created_at = models.DateTimeField(db_default=Now())
    updated_at = models.DateTimeField(db_default=Now())
    deleted_at = models.DateTimeField(null=True, blank=True)
