from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from events.models import Event
from users.models import User
from .forms import RegistrationForm
from .models import Category, Registration


class DummyCategory:
    """
    Simulates a Category instance for tests without DB load.

    Attributes:
        min_age: Minimum age.
        max_age: Maximum age.
        gender: 'M', 'F' or 'X'.
    """

    def __init__(self, min_age=None, max_age=None, gender='X'):
        self.min_age = min_age
        self.max_age = max_age
        self.gender = gender


class DummyUser:
    """
    Simulates a user with birth_date and sex attributes.

        Attributes:
            birth_date: Date of birth.
            sex: 'M' or 'F'.
    """

    def __init__(self, birth_date=None, sex='M'):
        self.birth_date = birth_date
        self.sex = sex


class RegistrationFormTests(TestCase):
    """
    Tests RegistrationForm validation in various scenarios:

    - valid data
    - missing date of birth
    - too young/too old user
    - gender mismatch
    - category with 'X' (doesn't matter)
    - no category selected
    """

    def setUp(self):
        """
        Sets today's date for age calculations.
        """

        self.today = date.today()

    def test_valid_data(self):
        """
        It verifies that the form is valid for users of the correct age and
        gender.
        """

        category = Category.objects.create(
            min_age=18, max_age=30, gender='M', name='Test'
        )
        user = DummyUser(
            birth_date=self.today.replace(year=self.today.year - 25),
            sex='M'
        )
        form = RegistrationForm(data={'category': category.pk}, user=user)
        self.assertTrue(form.is_valid())

    def test_missing_birth_date(self):
        """
        It verifies that a missing date of birth returns an invalid form with
        an error.
        """

        category = Category.objects.create(
            min_age=18, max_age=30, gender='M', name='Test'
        )
        user = DummyUser(birth_date=None, sex='M')
        form = RegistrationForm(data={'category': category.pk}, user=user)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Uživatel nemá vyplněné datum narození.",
            form.non_field_errors()[0]
        )

    def test_too_young(self):
        """
        It verifies that an age below min_age returns an invalid form with a
        corresponding error.
        """

        category = Category.objects.create(
            min_age=18, max_age=30, gender='M', name='Test'
        )
        user = DummyUser(
            birth_date=self.today.replace(year=self.today.year - 17),
            sex='M'
        )
        form = RegistrationForm(data={'category': category.pk}, user=user)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Vašemu věku neodpovídá vybraná kategorie.",
            form.non_field_errors()[0]
        )

    def test_too_old(self):
        """
        It verifies that an age above max_age returns an invalid form with a
        corresponding error.
        """

        category = Category.objects.create(
            min_age=18, max_age=30, gender='M', name='Test'
        )
        user = DummyUser(
            birth_date=self.today.replace(year=self.today.year - 31),
            sex='M'
        )
        form = RegistrationForm(data={'category': category.pk}, user=user)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Vašemu věku neodpovídá vybraná kategorie.",
            form.non_field_errors()[0]
        )

    def test_gender_mismatch(self):
        """
        Verify that gender mismatch returns an invalid form with an error.
        """

        category = Category.objects.create(
            min_age=18, max_age=30, gender='F', name='Test'
        )
        user = DummyUser(
            birth_date=self.today.replace(year=self.today.year - 25),
            sex='M'
        )
        form = RegistrationForm(data={'category': category.pk}, user=user)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Vaše pohlaví neodpovídá vybrané kategorii.",
            form.non_field_errors()[0]
        )

    def test_gender_any(self):
        """
        Verify that a category with gender='X' accepts any gender.
        """

        category = Category.objects.create(
            min_age=18, max_age=30, gender='X', name='Test'
        )
        user = DummyUser(
            birth_date=self.today.replace(year=self.today.year - 25),
            sex='F'
        )
        form = RegistrationForm(data={'category': category.pk}, user=user)
        self.assertTrue(form.is_valid())

    def test_no_category_selected(self):
        """
        Verify that not selecting a category returns an error on the
        'category' field.
        """

        user = DummyUser(
            birth_date=self.today.replace(year=self.today.year - 25),
            sex='M'
        )
        form = RegistrationForm(data={'category': None}, user=user)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Toto pole je třeba vyplnit.",
            form.errors['category'][0]
        )


class RegistrationModelTest(TestCase):
    """
    Tests the validation of the Registration model.

    Verifies that a valid registration cannot be created without a user or an
    event.
    """

    def setUp(self):
        """
        Prepares common objects for all tests:

        - user (self.user)
        - event (self. Event)
        """

        self.user = User.objects.create(email='test@example.com')
        self.event = Event.objects.create(
            name_event='Test Event',
            date_event='2025-07-06',
            description='Testovací popis',
            start_time='10:00',
            distance=10,
            country='Česká republika',
            city='Praha',
            region='hlavní město Praha',
            race_type='Silnice',
            organizer=self.user
        )
        self.category = Category.objects.create(name='Test kategorie')

    def test_registration_without_user_is_invalid(self):
        """
        Verify that registration without an assigned user will throw a
        ValidationError when calling full_clean().
        """

        registration = Registration(id_event=self.event)
        with self.assertRaises(ValidationError):
            registration.full_clean()

    def test_registration_without_event_is_invalid(self):
        """
        Verify that registration without an associated event will throw a
        ValidationError when calling full_clean().
        """

        registration = Registration(id_user=self.user)
        with self.assertRaises(ValidationError):
            registration.full_clean()

    def test_registration_unique_constraint(self):
        """
        Verify that a user cannot register for the same event twice.
        """

        Registration.objects.create(
            id_user=self.user,
            id_event=self.event,
            category=self.category
        )
        with self.assertRaises(Exception):
            Registration.objects.create(
                id_user=self.user,
                id_event=self.event,
                category=self.category
            )
