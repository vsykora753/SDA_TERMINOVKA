from django.db import models
from django.conf import settings
# Create your models here.

class Event(models.Model):
    date_event = models.DateField(verbose_name='Datum události')
    name_event = models.CharField(
    max_length=255,    
    verbose_name='Název události'
    )
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
    limit_choices_to={'role': 'O'},
    related_name='organized_events'
)


    class Meta:
        """
        Meta class for Event model.
        defines ordering of the model.
        1. date_event - sorts events by date
        
        """
        ordering = ['date_event']

        def __str__(self):
            return self.name_event

 