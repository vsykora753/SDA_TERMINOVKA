from django.db import models
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    variable_symbol = models.CharField(max_length=10, default=0000000000)
    account_number = models.CharField(max_length=24, default="1234567890")
    bank_code = models.CharField(max_length=4, default="0100")
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def create_spayd_string(self):
        """Vytvoří SPAYD string podle české specifikace pro QR platby"""
        # Formátování částky na 2 desetinná místa
        amount = f"{float(self.amount):.2f}"

        # Sestavení základních údajů pro platbu
        account = f"CZ{self.account_number}{self.bank_code}"

        # Sestavení SPAYD stringu
        spayd_parts = [
            "SPD*1.0",  # Verze SPAYD
            f"ACC:{account}",  # Číslo účtu
            f"AM:{amount}",  # Částka
            "CC:CZK",  # Měna
            f"VS:{self.variable_symbol}"  # Variabilní symbol
        ]

        return "*".join(spayd_parts)

    def generate_qr_code(self):
        # Vytvoření QR kódu z SPAYD stringu
        spayd_string = self.create_spayd_string()
        qr_image = qrcode.make(spayd_string)

        # Uložení QR kódu do BytesIO
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')

        # Vytvoření názvu souboru
        filename = f'qr_payment_{self.variable_symbol}.png'

        # Uložení do modelu
        self.qr_code.save(
            filename,
            ContentFile(buffer.getvalue()),
            save=False
        )
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.qr_code:
            self.generate_qr_code()

    def __str__(self):
        return f"Platba {self.amount} Kč (VS: {self.variable_symbol})"