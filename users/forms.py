from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from datetime import date
from dateutil.relativedelta import relativedelta

class LoginForm(forms.Form):
    email = forms.EmailField(label='Emailová adresa')
    password = forms.CharField(label='Heslo', widget=forms.PasswordInput)
                                    
class RegisterForm(UserCreationForm):
    birth_date = forms.DateField(
        label='Datum narození',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'birth_date',
            'sex',
            'password1',
            'password2',
        ]
        labels = {
            'email': 'Emailová adresa',
            'first_name': 'Křestní jméno',
            'last_name': 'Příjmení',
            'birth_date': 'Datum narození',
            'sex': 'Pohlaví',
            'password1': 'Heslo',
            'password2': 'Potvrzení hesla',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Tento email je již zaregistrovaný.")
        return email

    def clean_user_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            age = relativedelta(date.today(), birth_date).years
            if age < 18:
                raise forms.ValidationError("Musíte být starší 18 let pro registraci.")
        return birth_date