from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("admin", "Admin"),
    )

    email = models.EmailField(
        unique=True
    )

    full_name = models.CharField(
        max_length=255
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer"
    )

    address=models.TextField(blank=True,null=True)

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    is_email_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def __str__(self):
        return self.email