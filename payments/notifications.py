from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_payment_confirmation(payment):
    """Odeslání potvrzení o platbě"""
    subject = f'Potvrzení platby - {payment.id_event.name}'
    message = render_to_string(
        'payments/email/payment_confirmation.html',
        {'payment': payment}
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [payment.id_user.email],
        html_message=message
    )


def send_payment_reminder(payment):
    """Odeslání připomínky platby"""
    subject = f'Připomínka platby - {payment.id_event.name}'
    message = render_to_string(
        'payments/email/payment_reminder.html',
        {'payment': payment}
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [payment.id_user.email],
        html_message=message
    )
