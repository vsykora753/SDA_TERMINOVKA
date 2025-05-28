from django.db import models
from events.models import Event
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Payment(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='payments',verbose_name='id_uživatele',default=1)
    id_event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='payments',verbose_name='id_události',default=1)
    id_registration = models.ForeignKey('registrations.Registration',on_delete=models.CASCADE,related_name='payments',verbose_name='id_registrace',default=1)
    payment_amount = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Částka')
    payment_status = models.CharField(max_length=15,choices=[('Paid', 'Zaplaceno'), ('Unpaid', 'Nezaplaceno')],verbose_name='Stav platby')
    payment_date = models.DateField(verbose_name='Datum platby')
    QR_code = models.CharField(max_length=255,verbose_name='QR kód')


    def __str__(self):
        return f"{self.id_user} - {self.id_event} - {self.payment_amount} - {self.payment_status} - {self.payment_date} - {self.QR_code}"
   
    class Meta:
        ordering = ['payment_date']
        unique_together = ('id_user', 'id_event')
        verbose_name = 'Platba'
        verbose_name_plural = 'Platby'


