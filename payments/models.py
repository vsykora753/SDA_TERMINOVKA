from django.db import models
from events.models import Event
from django.contrib.auth.models import User
from django.conf import settings


class Payment(models.Model):
    """
    Represents a payment record within the system.

    This class defines the structure for payment information, including
    associations with users, events, and registrations. It also tracks
    various details of payments, such as the amount, status, date, and
    related QR code. The class ensures the uniqueness of user-event payment
    combinations and provides an order for payment records based on their
    payment date.

    Attributes:
        id (AutoField): The unique identifier for the payment.
            Automatically generated.
        id_user (ForeignKey): A foreign key referencing the user associated
            with the payment.
        id_event (ForeignKey): A foreign key referencing the event associated
            with the payment.
        id_registration (ForeignKey): A foreign key referencing the
            registration linked to the payment.
        payment_amount (DecimalField): The amount of the payment with up to
            10 digits, including 2 decimal places.
        payment_status (CharField): Indicates the status of the payment,
            either 'Paid' or 'Unpaid'.
        payment_date (DateField): The date when the payment was made.
        QR_code (CharField): A string representation of the payment's QR code
            for identification or processing.
    """

    id = models.AutoField(primary_key=True,auto_created=True)
    id_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='id_uživatele',
        default=1
    )
    id_event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='id_události',
        default=1
    )
    id_registration = models.ForeignKey(
        'registrations.Registration',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='id_registrace',
        default=1
    )
    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Částka'
    )
    payment_status = models.CharField(
        max_length=15,
        choices=[
            ('Paid', 'Zaplaceno'),
            ('Unpaid', 'Nezaplaceno')
        ],
        verbose_name='Stav platby'
    )
    payment_date = models.DateField(verbose_name='Datum platby')
    QR_code = models.CharField(max_length=255,verbose_name='QR kód')

    def __str__(self):
        return (f"{self.id_user} - "
                f"{self.id_event} - "
                f"{self.payment_amount} - "
                f"{self.payment_status} - "
                f"{self.payment_date} - "
                f"{self.QR_code}"
                )
   
    class Meta:
        ordering = ['payment_date']
        unique_together = ('id_user', 'id_event')
        verbose_name = 'Platba'
        verbose_name_plural = 'Platby'
