from datetime import date

from django.test import TestCase

from .forms import RegistrationForm
from .models import Category


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
