from django.apps import AppConfig


class EventsConfig(AppConfig):
    """
    Configuration class for the 'events' application.

    This class is responsible for defining the configuration for the
    Django application named 'events'. It sets the default primary key
    field type for models and specifies the application name.

    Attributes:
        default_auto_field (str): The default type of the primary key field
            for models in this application.
        name (str): The name of the application.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "events"
