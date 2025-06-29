from django.db import models
from events.models import Event
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Registration(models.Model):

    id = models.AutoField(primary_key=True,auto_created=True)
    id_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
        related_name='registrations',verbose_name='id_uživatele',default=1)
    id_event = models.ForeignKey(
        Event,on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='id_události',default=1)
    registration_date = models.DateTimeField(
        auto_now_add=True,verbose_name='Datum registrace')
    
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
    name = models.CharField(max_length=50, 
        verbose_name='Název kategorie')
    min_age = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Minimální věk'
        )
    max_age = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Maximální věk'
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

