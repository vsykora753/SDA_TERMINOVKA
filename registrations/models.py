from django.db import models
from events.models import Event
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Registration(models.Model):

    id = models.AutoField(primary_key=True,auto_created=True)
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='registrations',verbose_name='id_uživatele',default=1)
    id_event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='registrations',verbose_name='id_události',default=1)
    registration_date = models.DateTimeField(auto_now_add=True,verbose_name='Datum registrace')
    category = models.CharField(max_length=7,
                                choices=[('M40', 'Muži do 40 let '), ('V', 'Veteráni'), 
                                ('W40', 'Ženy do 40 let'), ('W0', 'Veteránky'),  ('Junior', 'Dorostenci')], verbose_name='Kategorie'    ) 
    
    def __str__(self):
            return f"{self.id_user} - {self.id_event}"
            
    class Meta:
        ordering = ['registration_date']
        unique_together = ('id_user', 'id_event')
        verbose_name = 'Registrace'
        verbose_name_plural = 'Registrace'
