from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from datetime import date


class UserManager(BaseUserManager):
    """
    Správce uživatelských účtů rozšiřující Django BaseUserManager.

    Tato třída poskytuje metody pro vytváření běžných uživatelů a
    superuživatelů s e-mailovou adresou jako hlavním identifikátorem místo
    tradičního uživatelského jména.

    Attributes:
        Dědí všechny atributy z BaseUserManager
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Vytvoří a uloží nového běžného uživatele s daným emailem a heslem.

        Args:
            email: Emailová adresa uživatele
            password: Heslo uživatele (volitelné)
            **extra_fields: Další pole pro uživatele

        Returns:
            User: Nově vytvořený uživatelský účet

        Raises:
            ValueError: Pokud není zadán email
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
        Vytvoří a uloží nového superuživatele s administrátorskými právy.

        Automaticky nastaví výchozí hodnoty pro povinná pole a administrativní
        oprávnění.

        Args:
            email (str): E-mailová adresa superuživatele
            password (str, optional): Heslo superuživatele. Výchozí None.
            **extra_fields: Dodatečná pole pro model uživatele

        Returns:
            User: Nově vytvořený superuživatelský objekt

        Example:
            >>> UserManager().create_superuser('admin@example.com', 'admin123')
            <User: admin@example.com>

        Note:
            Automaticky nastavuje následující výchozí hodnoty:

            - is_staff = True
            - is_superuser = True
            - birth_date = date(2000, 1, 1)
            - role = 'A' (Admin)
            - další povinná pole pro profil
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
    Vlastní uživatelský model rozšiřující Django AbstractBaseUser a
    PermissionsMixin.

    Model reprezentuje uživatele v systému s různými rolemi (běžec,
    organizátor, admin). Používá email jako primární způsob přihlášení místo
    uživatelského jména.

    Attributes:
        email (EmailField): Unikátní emailová adresa uživatele
        role (CharField): Role uživatele (R-běžec, O-organizátor, A-admin)
        first_name (CharField): Křestní jméno uživatele
        last_name (CharField): Příjmení uživatele
        birth_date (DateField): Datum narození
        sex (CharField): Pohlaví uživatele (M-muž, F-žena)
        organization_name (CharField): Název organizace (volitelné)
        website (URLField): Webová stránka (volitelné)
        is_active (BooleanField): Indikátor aktivního účtu
        is_staff (BooleanField): Příznak pro přístup do admin rozhraní

    Note:
        Model používá vlastní UserManager pro vytváření uživatelů a
        superuživatelů.

        Vyžadována jsou pole: role, first_name, last_name, birth_date a sex.
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
        Vrací string reprezentaci uživatelského objektu.

        Returns:
            str: Emailová adresa uživatele
        """
        return self.email

    class Meta:
        """
        Metadata pro model User.

        Attributes:
            verbose_name (str): Název modelu v jednotném čísle pro admin rozhraní
            verbose_name_plural (str): Název modelu v množném čísle pro admin rozhraní
        """
        verbose_name = "uživatel"
        verbose_name_plural = "uživatelé"
