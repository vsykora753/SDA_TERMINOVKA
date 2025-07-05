from django.db import models
from django.conf import settings


class Event(models.Model):
    """
    Represents a racing event with key information about the location, time
    and organizer.

    Attributes:
        date_event: Date of the event.
        name_event: Name of the event, max. 255 characters.
        description: Detailed description of the event.
        start_time: Start time of the event.
        distance: Distance in meters.
        country: Country of the event (max. 50 characters).
        region: Region of the event, selected from predefined options.
        race_type: Race surface; choice between 'Road', 'Trail' or 'Mix'.
        proposition: URL of the event proposition can be left blank.
        start_fee: Starting fee amount in CZK can be left blank.
        organizer: User (role 'O') who organizes the event.
    """

    date_event = models.DateField(
        verbose_name='Datum události'
    )
    name_event = models.CharField(
        max_length=255,
        verbose_name='Název události'
    )
    description = models.TextField(
        verbose_name='Popis události'
    )
    start_time = models.TimeField(
        verbose_name='Čas startu'
    )
    distance = models.IntegerField(
        verbose_name='Vzdálenost'
    )
    country = models.CharField(
        max_length=50,
        verbose_name='Země'
    )
    city = models.CharField(
        max_length=50,
        verbose_name='Město'
    )
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
    race_type = models.CharField(
        max_length=7,
        choices=[
            ('Silnice', 'Silnice'),
            ('Trail', 'Trail'),
            ('Mix', 'Smíšený')
        ],
        verbose_name='Typ závodu - povrch'
    )
    proposition = models.URLField(
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
        limit_choices_to={'role': 'O'},
        related_name='organized_events'
    )


    class Meta:
        """
        Default sorting by event date (`['date_event']`).
        """

        ordering = ['date_event']

    def __str__(self):
        """
        Returns:
            The event name for the instance representation.

        """

        return self.name_event
