from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import date
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Uživatel musí mít emailovou adresu.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('birth_date',date(2000, 1, 1))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('R', 'Runner'),
        ('O', 'Organizátor'),
        ('A', 'Admin'),
    ]

    # společné pro všechny (uživatel,organizátor, admin)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128,null=False,blank=False)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)

    # pole specifické pro fyzické osoby (běžce)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=60, null=False, blank=False)
    birth_date = models.DateField(null=False, blank=False)
    sex = models.CharField(max_length=1, choices=[('M', 'Muž'), ('F', 'Žena')], null=False, blank=False)

    # pole specifické pro organizátory (povětšinou právniké osoby, sdružení)
    organization_name = models.CharField(max_length=100, null=False, blank=False)
    website = models.URLField(null=False, blank=False)

    # Django interní pole
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "uživatel"
        verbose_name_plural = "uživatelé"
