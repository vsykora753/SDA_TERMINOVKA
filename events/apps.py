from django.apps import AppConfig


class EventsConfig(AppConfig):
    """
    Configures the events application within a Django project.

    Attributes:
        default_auto_field: The fully qualified name of the field that Django
        will use as the default primary key for new models (BigAutoField).
        name: The Python import path of the application, here 'events'.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "events"
