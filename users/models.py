from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from datetime import date

class UserManager(BaseUserManager):
    """

    Manages user creation and administration tasks.

    This class provides methods for creating regular users and superusers
    with specific attributes required for managing accounts. It ensures
    that all required attributes, including default and additional values,
    are properly configured and saved to the database.

    Attributes:
        model (Model): The user model that the manager works with.

    Methods:
        create_user(email: str, password: str | None = None, **extra_fields)
            -> User: Creates and saves a regular user with the provided email
            and password.
        create_superuser(email: str, password: str | None = None,
            **extra_fields) -> User: Creates and saves a superuser with full
            administrative permissions.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a new user with the provided email and password.

        This function validates that an email is provided, normalizes the email
        address, hashes the password, and saves the user object to the database.
        Additional fields can also be passed as keyword arguments to be included
        during user creation.
        This function validates that an email is provided, normalizes the
        email address, hashes the password, and saves the user object to the
        database. Additional fields can also be passed as keyword arguments to
        be included during user creation.

        Args:
            email: User's email address. This is required.
            password: User's raw password. Defaults to None.
            **extra_fields: Additional fields to include in the user object.

        Returns:
            The created user object.More actions

        Raises:
            ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError("Uživatel musí mít emailovou adresu.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # HASHOVÁNÍ hesla zde
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with the specified email, password, and additional
        fields. This method ensures that the user has administrative permissions by setting
        default values for these permissions and other required attributes.
        Creates and returns a superuser with the specified email, password,
        and additional fields. This method ensures that the user has
        administrative permissions by setting default values for these
        permissions and other required attributes.

        Args:
           
            email: The email address of the superuser. It is required for user
                creation.
            password: The password for the superuser. Defaults to None if not
                provided.
            **extra_fields: Additional fields for customizing the superuser,
                such as 'first_name', 'last_name', 'organization_name', etc.
                These may include permissions and other attributes essential
                for the superuser role.

        Returns:
            User: The created superuser instance.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("birth_date", date(2000, 1, 1))
        extra_fields.setdefault("first_name", "Admin")
        extra_fields.setdefault("last_name", "Admin")
        extra_fields.setdefault("sex", "M")
        extra_fields.setdefault("organization_name", "AdminOrg")
        extra_fields.setdefault("website", "https://admin.cz")
        extra_fields.setdefault("role", "A")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Represents a user with authentication and role-based privileges.

    This class represents a user model that inherits from the AbstractBaseUser
    and PermissionsMixin to handle user authentication, role assignment, and
    permissions. It uses an email address as the unique identifier for the
    user and includes additional fields for personal and organizational
    information. The model is intended to support role-based access control
    and is managed through an external UserManager class.

    Attributes:
        ROLE_CHOICES (list): A list of tuples defining the possible user roles.
            Each tuple contains a short code for the role and its verbose name.
        email (models.EmailField): The email address of the user, used as the
            unique identifier.
        role (models.CharField): The role of the user, chosen fromAdd commentMore actions
            ROLE_CHOICES.
        first_name (models.CharField): The first name of the user.Add commentMore actions
        last_name (models.CharField): The last name of the user.
        birth_date (models.DateField): The birthdate of the user, nullable and
            optional.
        sex (models.CharField): The gender of the user, chosen from predefinedAdd commentMore actions
            options.
        organization_name (models.CharField): The name of the organization the
            user is affiliated with, nullable and optional.
        website (models.URLField): A URL representing the user's orAdd commentMore actions
            organization's website, nullable and optional.
        is_active (models.BooleanField): Specifies whether the account is
            active or deactivated.
        is_staff (models.BooleanField): Indicates whether the user has staff
            privileges.Add commentMore actions
        objects (UserManager): A custom user manager for handling user-related
            queries and operations
        USERNAME_FIELD (str): The field used as the username forAdd commentMore actions
            authentication, which is set to 'email'.
        REQUIRED_FIELDS (list): A list of fields required for creating a user,
            excluding the username and password.Add commentMore actions
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

    USERNAME_FIELD = "email"  # klíčové: email jako uživatelské jméno
    REQUIRED_FIELDS = ["role", "first_name", "last_name", "birth_date", "sex"]

    def __str__(self):
        """
        Returns the string representation of the instance.
        This method provides a human-readable string representation of theAdd commentMore actions
        object, typically used for debugging or displaying the instance in a
        user-friendly format.

        Returns:
            str: A string representation of the instance , specifically the email of attribute.
        """
        return self.email

    class Meta:
        """
        Represents a user entity.

        Represents the user model in the application. It defines the
        properties related to a user and is used for data management and user
        representation in the system.

        Attributes:
            verbose_name (str): Singular name for the user, used for
                presentation.
            verbose_name_plural (str): Plural name for the user, used for
                presentation of multiple users.Add commentMore actions
        """
        verbose_name = "uživatel"
        verbose_name_plural = "uživatelé"