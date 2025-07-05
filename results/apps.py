from django.apps import AppConfig


class ResultsConfig(AppConfig):
    """
    Configures the results application within a Django project.

    Attributes:
        default_auto_field: The fully qualified name of the field that Django
        will use as the default primary key for new models.
        name: The Python import path of the application – 'results'.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "results"
