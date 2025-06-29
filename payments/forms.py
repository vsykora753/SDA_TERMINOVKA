from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'variable_symbol', 'account_number', 'bank_code']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'variable_symbol': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_code': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'amount': 'Částka (Kč)',
            'variable_symbol': 'Variabilní symbol',
            'account_number': 'Číslo účtu',
            'bank_code': 'Kód banky'
        }