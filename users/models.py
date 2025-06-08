from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from datetime import date

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Uživatel musí mít emailovou adresu.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # HASHOVÁNÍ hesla zde
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('birth_date', date(2000, 1, 1))
        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'Admin')
        extra_fields.setdefault('sex', 'M')
        extra_fields.setdefault('organization_name', 'AdminOrg')
        extra_fields.setdefault('website', 'https://admin.cz')
        extra_fields.setdefault('role', 'A')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('R', 'Runner'),
        ('O', 'Organizátor'),
        ('A', 'Admin'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=60)
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=[('M', 'Muž'), ('F', 'Žena')])

    organization_name = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'        # klíčové: email jako uživatelské jméno
    REQUIRED_FIELDS = ['role', 'first_name', 'last_name', 'birth_date', 'sex']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "uživatel"
        verbose_name_plural = "uživatelé"