from django.apps import AppConfig


class RegistrationsConfig(AppConfig):
    """
    Configures the registrations application within a Django project.

    Attributes:
        default_auto_field: Default primary key type (here BigAutoField for
        auto-numbering IDs).
        name: Python import path of the application — 'registrations'.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "registrations"
