from datetime import date

from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from events.models import Event
from .models import User


class LoginForm(forms.Form):
    """
    Handles user login via email and password.

    Validates email and password combination using authenticate(), and if
    successful saves user to self. User.
    """

    email = forms.EmailField(label='Emailová adresa')
    password = forms.CharField(label='Heslo', widget=forms.PasswordInput)

    def clean(self):
        """
        Verify that the email and password belong to an existing user.

        Raises:
            forms.ValidationError: if the combination is not valid.

        Returns:
            The sanitized form data (email, password).
        """

        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Neplatné přihlašovací údaje.")
            self.user = user
        return cleaned_data


class RegisterForm(UserCreationForm):
    """
    Registers a new runner (role 'R') with email and age validation.

    Adds the fields birth_date, organization_name, and website.
    """

    birth_date = forms.DateField(
        label="Datum narození",
        widget=forms.DateInput(attrs={"type": "date"})
    )
    organization_name = forms.CharField(
        label="Název organizace",
        required=False
    )
    website = forms.URLField(label="Webová stránka", required=False)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "sex",
            "organization_name",
            "website",
            "password1",
            "password2",
        ]
        labels = {
            "email": "Emailová adresa",
            "first_name": "Křestní jméno",
            "last_name": "Příjmení",
            "birth_date": "Datum narození",
            "sex": "Pohlaví",
            "organization_name": "Název organizace",
            "website": "Webová stránka",
            "password1": "Heslo",
            "password2": "Potvrzení hesla",
        }

    def clean_email(self):
        """
        Ensures the uniqueness of the email in the system.

        Raises:
            forms.ValidationError: if the email already exists.

        Returns:
            The cleaned email.
        """

        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Tento email je již zaregistrovaný.")
        return email

    def clean_birth_date(self):
        """
        Checks that the user is over 18 years old and the date is not in the
        future.

        Raises:
            forms.ValidationError: on missing, future, or too young date.

        Returns:
            The sanitized date of birth.
        """

        birth_date = self.cleaned_data.get('birth_date')
        today = date.today()
        if not birth_date:
            raise forms.ValidationError("Datum narození je povinné.")

        if birth_date > today:
            raise forms.ValidationError(
                "Datum narození nemůže být v budoucnosti.")
        if birth_date:
            age = relativedelta(date.today(), birth_date).years
            if age < 18:
                raise forms.ValidationError(
                    "Musíte být starší 18 let pro registraci.")
        return birth_date

    def save(self, commit=True):
        """
        Sets the role 'R' and saves the new user.

        Args:
            commit (bool): whether to write the user to the DB now.

        Returns:
            The newly created user with the fields filled in.
        """

        user = super().save(commit=False)
        user.birth_date = self.cleaned_data.get("birth_date")
        user.organization_name = self.cleaned_data.get("organization_name")
        user.website = self.cleaned_data.get("website")
        user.role = "R"
        if commit:
            user.save()
        return user


class OrganizerRegisterForm(UserCreationForm):
    """
    Registers a new organizer (role 'O').

    Contains the required organization_name field.
    """

    organization_name = forms.CharField(
        label="Název organizace",
        required=True
    )
    organization_name = forms.CharField(
        label='Název organizace',
        required=True
    )

    class Meta:
        model = User
        fields = [
            "email",
            "organization_name",
            "password1",
            "password2",
        ]
        labels = {
            "email": "Emailová adresa",
            "organization_name": "Název organizace",
            "password1": "Heslo",
            "password2": "Potvrzení hesla",
        }

    def clean_email(self):
        """
        It will also provide a unique email for the organizers.

        Raises:
            forms.ValidationError: if the email already exists.

        Returns:
            Cleaned email
        """

        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Tento email je již zaregistrovaný.")
        return email

    def save(self, commit=True):
        """
        Sets the role 'O' and saves the organizer.

        Args:
            commit (bool): whether to write the user to the DB now.

        Returns:
            The newly created organizer.
        """

        user = super().save(commit=False)
        user.organization_name = self.cleaned_data.get("organization_name")
        user.role = "O"  # nastavíme roli organizátora
        if commit:
            user.save()
        return user


class OrganizerEventForm(forms.ModelForm):
    """
    Form for the organizer to create or edit an event.

    Validates the event date, start time, distance, entry fee, and region.
    """

    class Meta:
        model = Event
        fields = [
            'date_event',
            'name_event',
            'description',
            'start_time',
            'distance',
            'country',
            'city',
            'region',
            'race_type',
            'proposition',
            'start_fee',
        ]
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'rows': 5,
                    'cols': 80,
                    'style': 'width: 100%;',
                    'placeholder': 'Popiš událost...'
                }
            )
        }
        labels = {
            'date_event': 'Datum události',
            'name_event': 'Název události',
            'description': 'Popis události',
            'start_time': 'Čas startu',
            'distance': 'Vzdálenost',
            'country': 'Země',
            'city': 'Město',
            'region': 'Kraj',
            'race_type': 'Typ závodu - povrch',
            'proposition': 'Propozice',
            'start_fee': 'Startovné',
        }

    def clean_date_event(self):
        """
        Checks that the event date is not in the past.

        Raises:
            forms.ValidationError: if date_event < today.

        Returns:
            The sanitized event date.
        """

        date_event = self.cleaned_data.get('date_event')
        if date_event and date_event < date.today():
            raise forms.ValidationError(
                "Datum události nemůže být v minulosti. "
                "Zvolte prosím platné datum."
            )
        return date_event

    def clean_start_time(self):
        """
        Validates the start_time hours and minutes.

        Raises:
            forms.ValidationError: if not 00:00–23:59.

        Returns:
            The cleared start time.
        """

        start_time = self.cleaned_data.get('start_time')
        if start_time:
            if (start_time.hour < 0 or start_time.hour > 23 or
                    start_time.minute < 0 or start_time.minute > 59
            ):
                raise forms.ValidationError(
                    "Čas startu musí být v platném formátu (HH:MM)."
                )
        return start_time

    def clean_distance(self):
        """
        Checks that the distance is a positive number.

        Raises:
            forms.ValidationError: if distance ≤ 0.

        Returns:
            The cleaned distance (meters).
        """

        distance = self.cleaned_data.get('distance')
        if distance is not None and distance <= 0:
            raise forms.ValidationError(
                "Vzdálenost musí být kladné číslo(v metrech)."
            )
        return distance

    def clean_start_fee(self):
        """
        Verify that the start fee is not negative and round it to a multiple
        of 10.

        Raises:
            forms.ValidationError: if start_fee < 0.

        Returns:
            The rounded start fee.
        """

        start_fee = self.cleaned_data.get('start_fee')
        if start_fee is not None and start_fee < 0:
            raise forms.ValidationError(
                "Startovné nemůže být záporné číslo."
            )
        if start_fee is not None:
            rounded_fee = round(start_fee / 10) * 10
            return rounded_fee

        return start_fee

    def clean_region(self):
        """
        Mandatory validation of region selection.

        Raises:
            forms.ValidationError: if region is not filled in.

        Returns:
            Cleaned region.
        """

        region = self.cleaned_data.get('region')
        if not region:
            raise forms.ValidationError("Kraj je povinný.")
        return region
