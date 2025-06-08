from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class EmailBackend(ModelBackend):
    """
    Custom authentication backend using email and password for user
    authentication.

    This class defines an authentication backend which allows users to
    authenticate via their email address and password instead of a username.
    It overrides the default authentication mechanism provided by Django.
    Users are retrieved from the database based on their email address and
    verified using their password. This backend also ensures that users are
    allowed to authenticate based on the criteria defined in the
    `user_can_authenticate` method.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticates a user based on their email and password. The function
        looks up the user by email and verifies the password. If successful,
        it checks if the user can be authenticated before returning the user
        object.

        Args:
            request: The HTTP request object.
            email: The email address of the user to authenticate.
            password: The password of the user to authenticate.
            **kwargs: Additional keyword arguments, if required.

        Returns:
            User: The authenticated user object if email and password match
            and authentication checks pass. Otherwise, returns None.
        """
        if email is None or password is None:
            return None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
