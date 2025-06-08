from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import User


class LoginForm(forms.Form):
    """
    A form for user login.

    This form is designed to handle user login by validating email and
    password inputs. It ensures that the provided credentials match an
    existing and valid user in the authentication backend.

    Attributes:
        email (forms.EmailField): A field to input the user's email address.
        password (forms.CharField): A field to input the user's password will
            be obscured as it uses the PasswordInput widget.
    """

    email = forms.EmailField(label="Emailová adresa")
    password = forms.CharField(label="Heslo", widget=forms.PasswordInput)

    def clean(self):
        """
        Validates and cleans the form data for user authentication. Ensures
        that the provided email and password are valid and correspond to an
        existing user. If both email and password are provided, attempts to
        authenticate the user. If authentication fails, it raises a validation
        error. The authenticated user is stored for further processing upon
        successful validation.

        Raises:
            forms.ValidationError: If authentication fails due to invalid
                email or password credentials.

        Returns:
            dict: A dictionary with the cleaned and validated data.
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
    A form for registering new users with extended fields.

    This form extends the default user creation form by adding additional
    fields for birthdate, organization name, and website. It also includes
    custom validation logic to ensure data integrity and business rules
    compliance, such as age verification.

    Attributes:
        birth_date: A required field for the user's date of birth.
        organization_name: An optional field for specifying the name of the
            organization associated with the user.
        website: An optional field for providing a URL to the user's or
            organization's website.
    """

    birth_date = forms.DateField(label="Datum narození",
                                 widget=forms.DateInput(attrs={"type": "date"})
    )
    organization_name = forms.CharField(label="Název organizace",
                                        required=False
    )
    website = forms.URLField(label="Webová stránka", required=False)

    class Meta:
        """
        Metadata configuration for the User model form.

        This class provides meta-options for defining the fields, labels, and
        structure of a form related to the User model. It specifies the
        fields to include in the form, the user-friendly labels for those
        fields, and is used to customize the form's representation and
        behavior.

        Attributes:
            model (Type[User]): The model that this form is based on.
            fields (list[str]): A list of field names included in the form.
            labels (dict[str, str]): A dictionary mapping field names to their
                human-readable labels.
        """

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
        Validates and processes the email field during form data cleaning.
        Ensures that the provided email is unique in the system and not
        already in use by another user.

        Raises:
            forms.ValidationError: If the provided email is already registered.

        Returns:
            str: The validated email address.
        """

        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Tento email je již zaregistrovaný.")
        return email

    def clean_birth_date(self):
        """
        Validates the birthdate input field, ensuring that it meets the
        following conditions:

        - A value for the birthdate must be provided.
        - The birthdate cannot be a future date.
        - The user's age, calculated from the birthdate, must be 18 years or
          older.

        Raises:
            forms.ValidationError: If the birthdate is not provided.
            forms.ValidationError: If the birthdate is in the future.
            forms.ValidationError: If the user is younger than 18 years old.

        Returns:
            datetime.date: The validated birthdate.
        """

        birth_date = self.cleaned_data.get("birth_date")
        today = datetime.date.today()  # TODO zjistit potencionální problém
        if not birth_date:
            raise forms.ValidationError("Datum narození je povinné.")

        if birth_date > today:
            raise forms.ValidationError(
                "Datum narození nemůže být v budoucnosti."
            )
        if birth_date:
            age = relativedelta(date.today(), birth_date).years
            if age < 18:
                raise forms.ValidationError(
                    "Musíte být starší 18 let pro registraci."
                )
        return birth_date

    def save(self, commit=True):
        """
        Saves the user instance with additional data processing and validation.

        This method overrides the save logic to include custom user attribute
        assignments before saving the instance. Attributes such as
        `birth_date`, `organization_name`, and `website` are populated from
        cleaned data. The user's `role` is explicitly set to "R" (runner). If
        the `commit` flag is set to False, the user instance is returned
        without being saved to the database.

        Args:
            commit (bool): A flag indicating whether the user instance should
                be saved to the database. If False, the instance is returned
                without saving.

        Returns:
            User: The user instance with updated attributes. If `commit` is
                True, the instance is saved before being returned.
        """

        user = super().save(commit=False)
        user.birth_date = self.cleaned_data.get("birth_date")
        user.organization_name = self.cleaned_data.get("organization_name")
        user.website = self.cleaned_data.get("website")
        user.role = "R"  # pevně nastavíme na běžce
        if commit:
            user.save()
        return user


class OrganizerRegisterForm(UserCreationForm):
    """
    A form for registering organizers with additional functionality.

    This form extends the standard UserCreationForm to include an additional
    field for the organization's name and custom validation for email
    uniqueness. It is used to create user accounts specifically for
    organizers, setting up their organization's name and assigning them the
    "Organizer" role.

    Attributes:
        organization_name (forms.CharField): A required field for the name of
            the organization.
    """

    organization_name = forms.CharField(label="Název organizace",
                                        required=True
    )

    class Meta:
        """
        Meta-information about form fields and their customization settings.

        This class defines the meta-configuration for a form. It specifies the
        model used, the fields involved in the form, and their respective
        labels for customization. The labels provide user-friendly names for
        the fields, making the form more intuitive and localized where needed.
        The configuration serves as a blueprint for maintaining the structure,
        names, and usability of the form fields.

        Attributes:
            model (type): Reference to the User model used by the form.
            fields (list of str): List of fields included in the form.
            labels (dict): Dictionary mapping field names to their
                corresponding user-friendly label names.
        """

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
        Validates and cleans the provided email.

        This method checks if the given email already exists in the database.
        If the email exists, it raises a validation error indicating that the
        email is already registered. Otherwise, it returns the cleaned email.

        Returns:
            str: The cleaned email address.

        Raises:
            forms.ValidationError: If the email is already registered.
        """

        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Tento email je již zaregistrovaný.")
        return email

    def save(self, commit=True):
        """
        Saves the user instance with additional customizations to the fields,
        such as setting the `organization_name` and default `role`. If the
        `commit` flag is True, saves the instance to the database. Otherwise,
        returns the modified instance without saving.

        Args:
            commit (bool): Indicates whether the changes to the user instance
                should be saved to the database. If False, the changes are
                only made to the instance in memory.

        Returns:
            User: The user instance, modified with the added or updated fields.
        """

        user = super().save(commit=False)
        user.organization_name = self.cleaned_data.get("organization_name")
        user.role = "O"
        if commit:
            user.save()
        return user
