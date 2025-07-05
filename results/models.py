from django.db import models
from events.models import Event
from django.contrib.auth.models import User
from django.conf import settings


class Result(models.Model):
    """
    Represents the user's resulting time for a specific event.

    Attributes:
        id: Primary key (automatically generated AutoField).
        id_user: User whose result is being stored.
        id_event: Event for which the result is recorded.
        year: Year of the event.
        result_time: Time achieved by the user during the event.
    """

    id = models.AutoField(
        primary_key=True,
        auto_created=True
    )
    id_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='id_uživatele',
        default=1
    )
    id_event = models.ForeignKey(
        Event,on_delete=models.CASCADE,
        related_name='results',
        verbose_name='id_události',
        default=1
    )
    year = models.IntegerField(verbose_name='Ročník')
    result_time = models.TimeField(verbose_name='Výsledný čas')

    def __str__(self):
            return f"{self.id_user} - {self.id_event} - {self.year}"

    class Meta:
        ordering = ['result_time']
        unique_together = ('id_user', 'id_event')
        verbose_name = 'Výsledek'
        verbose_name_plural = 'Výsledky'
