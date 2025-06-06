from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    email = forms.EmailField(label='Emailová adresa')
    password = forms.CharField(label='Heslo', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Neplatné přihlašovací údaje.")
            self.user = user  # ← uložit autentizovaného uživatele

        return cleaned_data

class RegisterForm(UserCreationForm):
    birth_date = forms.DateField(
        label='Datum narození',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    organization_name = forms.CharField(
        label='Název organizace',
        required=False
    )
    website = forms.URLField(
        label='Webová stránka',
        required=False
    )

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'birth_date',
            'sex',
            'organization_name',
            'website',
            'password1',
            'password2',
        ]
        labels = {
            'email': 'Emailová adresa',
            'first_name': 'Křestní jméno',
            'last_name': 'Příjmení',
            'birth_date': 'Datum narození',
            'sex': 'Pohlaví',
            'organization_name': 'Název organizace',
            'website': 'Webová stránka',
            'password1': 'Heslo',
            'password2': 'Potvrzení hesla',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Tento email je již zaregistrovaný.")
        return email

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        today = datetime.date.today()
        if not birth_date:
            raise forms.ValidationError("Datum narození je povinné.")

        if birth_date > today:
            raise forms.ValidationError("Datum narození nemůže být v budoucnosti.")
        if birth_date:
            age = relativedelta(date.today(), birth_date).years
            if age < 18:
                raise forms.ValidationError("Musíte být starší 18 let pro registraci.")
        return birth_date

    def save(self, commit=True):
        user = super().save(commit=False)
        user.birth_date = self.cleaned_data.get('birth_date')
        user.organization_name = self.cleaned_data.get('organization_name')
        user.website = self.cleaned_data.get('website')
        user.role = 'R'  # pevně nastavíme na běžce
        if commit:
            user.save()
        return user
    

class OrganizerRegisterForm(UserCreationForm):
    organization_name = forms.CharField(
        label='Název organizace',
        required=True
    )

    class Meta:
        model = User
        fields = [
            'email',
            'organization_name',
            'password1',
            'password2',
        ]
        labels = {
            'email': 'Emailová adresa',
            'organization_name': 'Název organizace',
            'password1': 'Heslo',
            'password2': 'Potvrzení hesla',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Tento email je již zaregistrovaný.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.organization_name = self.cleaned_data.get('organization_name')
        user.role = 'O'  # nastavíme roli organizátora
        if commit:
            user.save()
        return user
    