from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase


class UserModelTests(TestCase):
    """
    Tests the behavior of the custom user model.

    Verifies:
        - correct creation of regular user and superuser
        - email validation (empty or invalid)
    """

    def setUp(self):
        """
        Prepares test data:
            - one regular user
            - one superuser
            - one test permission per-User model
        """

        self.user_data = {
            'email': 'test@example.com',
            'password': 'SecurePass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = get_user_model().objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name']
        )
        self.admin_data = {
            'email': 'admin@example.com',
            'password': 'AdminPass123'
        }
        self.admin_user = get_user_model().objects.create_superuser(
            email=self.admin_data['email'],
            password=self.admin_data['password']
        )
        self.content_type = ContentType.objects.get_for_model(get_user_model())
        self.test_permission = Permission.objects.create(
            codename='can_test',
            name='Can Test',
            content_type=self.content_type
        )

    def tearDown(self):
        """
        Removes all users and test permissions after each test.
        """

        get_user_model().objects.all().delete()
        self.test_permission.delete()

    def test_create_user_success(self):
        """
        It verifies that the created regular user is active, but is not a
        staff or superuser.
        """

        user = get_user_model().objects.create_user(
            email='normal@user.com',
            password='testpass123'
        )
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """
        It verifies that the created superuser is active, both staff and
        superuser.
        """

        admin_user = get_user_model().objects.create_superuser(
            email='admin@user.com',
            password='testpass123'
        )
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_empty_email(self):
        """
        Verify that creating a user without an email will raise a ValueError.
        """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email="",
                password="testpass123"
            )

    def test_user_invalid_email(self):
        """
        Verify that creating a user with an invalid email will raise a
        ValueError.
        """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email="invalidmail",
                password="testpass123"
            )
