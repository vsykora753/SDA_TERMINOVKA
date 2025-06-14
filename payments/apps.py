from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    """
    Configuration class for the Payments application.

    This class represents the Django application configuration for the Payments
    module. It sets up the necessary parameters for the application, such as
    the default auto field and the application name. It is utilized by Django
    to configure and initialize the application during startup.

    Attributes:
        default_auto_field (str): Specifies the default type of primary key
            field to use for models in the application.
        name (str): The full Python path of the application, used for
            application registration in Django.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "payments"
