from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from events.models import Event
from datetime import date
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
        today = date.today()
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
    
class OrganizerEventForm(forms.ModelForm):
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
            'typ_race',
            'propozition',
            'start_fee',
        ]
        labels = {
            'date_event': 'Datum události',
            'name_event': 'Název události',
            'description': 'Popis události',
            'start_time': 'Čas startu',
            'distance': 'Vzdálenost',
            'country': 'Země',
            'city': 'Město',
            'region': 'Kraj',
            'typ_race': 'Typ závodu - povrch',
            'propozition': 'Propozice',
            'start_fee': 'Startovné',    
        }


    def clean_date_event(self):
        date_event = self.cleaned_data.get('date_event')
        if date_event and date_event < date.today():
            raise forms.ValidationError(
                "Datum události nemůže být v minulosti. "
                "Zvolte prosím platné datum."
            )
        return date_event
    
    def clean_start_time(self):
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
        distance = self.cleaned_data.get('distance')
        if distance is not None and distance <= 0:
            raise forms.ValidationError(
                "Vzdálenost musí být kladné číslo(v metrech)."
            )
        return distance
    
    def clean_start_fee(self):
        start_fee = self.cleaned_data.get('start_fee')
        if start_fee is not None and start_fee < 0:
            raise forms.ValidationError(                
                "Startovné nemůže být záporné číslo."
            )
        if start_fee is not None:
            rounded_fee = round(start_fee/ 10) * 10
            return rounded_fee
        
        return start_fee
    def clean_region(self):
        region = self.cleaned_data.get('region')
        if not region:
            raise forms.ValidationError("Kraj je povinný.")
        return region
    
