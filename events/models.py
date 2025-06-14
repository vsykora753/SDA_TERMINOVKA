from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Event(models.Model):
    """
    Represents an event with detailed information including date, name,
    location, and other specifics.

    This model describes an event entity, which includes details such as the
    event's date, name, brief description, start time, distance, location
    (country, city, region), race type, and other optional or additional
    details like proposition and start fee. It associates an organizer with
    the event who is restricted to users with a specific role. Events are
    ordered by their date.

    Attributes:
        date_event: The date when the event takes place.
        name_event: The name/title of the event.
        description: A brief description of the event.
        start_time: The starting time of the event.
        distance: The distance or length of the event.
        country: The country where the event is held.
        city: The city where the event takes place.
        region: The region in which the event is located. The region has
            predefined choices.
        typ_race: The type of surface for the race. This can be road, trail,
            or mixed with predefined choices.
        propozition: Optional. Additional propositions or details about the
            event.
        start_fee: Optional. The starting fee is required to participate in
            the event, if applicable.
        organizer: The organizer of the event. Linked to a user model
            restricted by a role.
    """

    date_event = models.DateField(verbose_name='Datum události')
    name_event = models.CharField(max_length=30, verbose_name='Název události')
    description = models.TextField(verbose_name='Popis události')
    start_time = models.TimeField(verbose_name='Čas startu')
    distance = models.IntegerField(verbose_name='Vzdálenost')
    country = models.CharField(max_length=50, verbose_name='Země')
    city = models.CharField(max_length=50, verbose_name='Město')
    region = models.CharField(
        max_length=100,
        choices=[
            ('hlavní město Praha', 'hlavní město Praha'),
            ('Středočeský kraj', 'Středočeský kraj'),
            ('Jihočeský kraj', 'Jihočeský kraj'),
            ('Plzeňský kraj', 'Plzeňský kraj'),
            ('Karlovarský kraj', 'Karlovarský kraj'),
            ('Ústecký kraj', 'Ústecký kraj'),
            ('Liberecký kraj', 'Liberecký kraj'),
            ('Královéhradecký kraj', 'Královéhradecký kraj'),
            ('Pardubický kraj', 'Pardubický kraj'),
            ('Kraj Vysočina', 'Kraj Vysočina'),
            ('Jihomoravský kraj', 'Jihomoravský kraj'),
            ('Olomoucký kraj', 'Olomoucký kraj'),
            ('Moravskoslezský kraj', 'Moravskoslezský kraj'),
            ('Zlínský kraj', 'Zlínský kraj')
        ],
        verbose_name='Kraj'
    )
    typ_race = models.CharField(
        max_length=7,
        choices=[
            ('Silnice', 'Silnice'),
            ('Trail', 'Trail'),
            ('Mix', 'Smíšený')
        ],
        verbose_name='Typ závodu - povrch'
    )
    propozition = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Propozice'
    )
    start_fee = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Startovné'
    )
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'O'}
    )
    class Meta:
        ordering = ['date_event']

    def __str__(self):
        return self.name_event


class Registration(models.Model):
    """
    Represents a user registration for an event.

    This model is used to link a user to a specific event that they have
    registered for. It includes the date and time of the registration,
    providing a record for event participation management. The model
    establishes foreign key relationships with both the user and the event.

    Attributes:
        user (ForeignKey): Reference to the user who registered for the event.
            Links to the `AUTH_USER_MODEL`.
        event (ForeignKey): Reference to the event for which the user
            registered. Links to the `Event` model.
        registered_at (DateTimeField): The date and time when the user
            registration was created. Automatically set to the current
            timestamp on creation.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
