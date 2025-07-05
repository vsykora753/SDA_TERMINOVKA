from django.db import models
from events.models import Event
from django.contrib.auth.models import User
from django.conf import settings


class Registration(models.Model):
    """
    Represents a user's registration for a specific racing event.

    Attributes:
        id: Primary key (automatically generated).
        id_user: The user registering for the event.
        id_event: The event the user is registering for.
        registration_date: Date and time the registration was created.
        category: The category (age/group) assigned to the registration.
    """

    id = models.AutoField(
        primary_key=True,
        auto_created=True
    )
    id_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='id_uživatele',
    )
    id_event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='id_události',
    )
    registration_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Datum registrace'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        verbose_name='Kategorie',
        related_name='registrations'
    )

    def __str__(self):
        return f"{self.id_user} - {self.id_event}"

    class Meta:
        ordering = ['registration_date']
        unique_together = ('id_user', 'id_event')
        verbose_name = 'Registrace'
        verbose_name_plural = 'Registrace'


class Category(models.Model):
    """
    Represents a competition category based on age and gender.

    Attributes:
        name: Category name (e.g. "Men 30-39").
        min_age: Minimum age to participate, optional.
        max_age: Maximum age to participate, optional.
        gender: Gender of participants; 'M' (male), 'F' (female), 'X' (unique).
    """

    name = models.CharField(
        max_length=50,
        verbose_name='Název kategorie'
    )
    min_age = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Minimální věk'
        )
    max_age = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Maximální věk'
        )
    gender = models.CharField(
        max_length=1, 
        choices=[('M', 'Muž'), ('F', 'Žena'), ('X', 'Nezáleží')], 
        default='X'
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategorie'
        verbose_name_plural = 'Kategorie'
