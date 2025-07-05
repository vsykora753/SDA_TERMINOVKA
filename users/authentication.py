from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class EmailBackend(ModelBackend):
    """
    Allows a user to log in using an email and password.

    Inherits from Django ModelBackend and overrides the authenticate method to
    require an email instead of a username.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Verify the existence of a user with the given email and password.

        Args:
            request: The original HTTP request.
            email: The specified email address.
            password: The specified password.
            **kwargs: Additional unused arguments.

        Returns:
            The logged-in user, if it exists and the password matches;
            otherwise None.
        """

        if email is None or password is None:
            return None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if (user.check_password(password) and
                    self.user_can_authenticate(user)):
                return user
        return None
