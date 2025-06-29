from django import forms
from .models import Registration
from datetime import date

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
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({
        'class': 'form-select',
        'aria-label': 'Kategorie registrace',
        'placeholder': 'Zvolte kategorii',
    })
    def clean(self):
        """
        Validates the selected category against the user's age and gender.

        - Checks if the user has a birth date provided; if not, raises a 
            validation error.
        - Calculates the user's age based on today's date.
        - Ensures the selected category's age boundaries (min_age, max_age)
            match the user's age.
        - Verifies that the category's gender restriction matches
            the user's gender,
            unless the category allows all genders ('X').

        Returns:
            dict: The cleaned data if all checks pass.

        Raises:
            forms.ValidationError: If the user's age or gender does not match
            the selected category,
            or if the user's birth date is missing.
        """
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        user = self.user

        if not category or not user:
            return cleaned_data

        # Věk uživatele
        if not user.birth_date:
            raise forms.ValidationError(
                "Uživatel nemá vyplněné datum narození.")
        
        today = date.today()
        age = today.year - user.birth_date.year - (
            (today.month, today.day) < 
            (user.birth_date.month, user.birth_date.day)
        )

        # Kontrola věku
        if category.min_age and age < category.min_age:
            raise forms.ValidationError(
                "Vašemu věku neodpovídá vybraná kategorie.")
        if category.max_age and age > category.max_age:
            raise forms.ValidationError(
                "Vašemu věku neodpovídá vybraná kategorie.")

        # Kontrola pohlaví
        if category.gender != 'X' and category.gender != user.sex:
            raise forms.ValidationError(
                "Vaše pohlaví neodpovídá vybrané kategorii.")
        return cleaned_data
    
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("Musíte vybrat kategorii.")
        return category
    