from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration for the 'users' application.

    This class provides the configuration setup for the 'users' application in
    a Django project. It specifies the default type for auto-generated primary
    keys and identifies the name of the application to be used internally by
    Django.

    Attributes:
        default_auto_field: Specifies the default field type for
            auto-generated primary keys in models within this application.
            Set to 'django.db.models.BigAutoField' to use 64-bit integer
            fields.
        name: Defines the internal application name used by Django. Set to
            'users' for this specific application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
