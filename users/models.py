from datetime import date

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models


class UserManager(BaseUserManager):
    """
    Manages user and superuser creation with email validation.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular user.

        Validates that the email is entered and in the correct format.

        Args:
            email: The user's unique email address.
            password: The user's password.
            **extra_fields: Additional fields of the User model.

        Returns:
            The newly created user.

        Raises:
            ValueError: If the email is missing or in an invalid format.
        """

        if not email:
            raise ValueError("Uživatel musí mít emailovou adresu.")

        try:
            email = self.normalize_email(email)
            validate_email(email)
        except ValidationError:
            raise ValueError("Neplatný formát emailu")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with role 'A' and default fields.

        Args:
            email: Superuser email address.
            password: Password.
            **extra_fields: Extra fields (set by is_staff, is_superuser,
            role,...).

        Returns:
            The newly created superuser.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault(
            "birth_date",
            date(2000, 1, 1)
        )
        extra_fields.setdefault("first_name", "Admin")
        extra_fields.setdefault("last_name", "Admin")
        extra_fields.setdefault("sex", "M")
        extra_fields.setdefault("organization_name", "AdminOrg")
        extra_fields.setdefault("website", "https://admin.cz")
        extra_fields.setdefault("role", "A")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model using email as USERNAME_FIELD.

    Contains the roles Runner, Organizer and Admin, and other profile fields.
    """

    ROLE_CHOICES = [
        ("R", "Runner"),
        ("O", "Organizátor"),
        ("A", "Admin"),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=60)
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=[("M", "Muž"), ("F", "Žena")])
    organization_name = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["role", "first_name", "last_name", "birth_date", "sex"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "uživatel"
        verbose_name_plural = "uživatelé"
