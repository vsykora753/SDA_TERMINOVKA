from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    """
    Form for user registration to an event. 
    Allows users to select a category for the event.    
    """
    class Meta:
        """
        Meta class for the RegistrationForm.
        Specifies the model and fields to be used in the form.  
        """

        model = Registration
        fields = ['category']  
        labels = {
            'category': 'Zvolte kategorii',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({
        'class': 'form-select',
        'aria-label': 'Kategorie registrace',
        'placeholder': 'Zvolte kategorii',
    })