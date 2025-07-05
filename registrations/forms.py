from datetime import date
from django import forms
from .models import Registration


class RegistrationForm(forms.ModelForm):
    """
    Form for user registration for an event by selecting a category.

    Attributes:
        user: The user who is registering (User | None).
    """

    class Meta:
        """
        Meta settings for RegistrationForm.

        Attributes:
            model: The Registration Model whose data is being stored.
            fields: List of fields that will be displayed in the form.
            labels: Custom labels for individual fields.
        """

        model = Registration
        fields = ['category']  
        labels = {'category': 'Zvolte kategorii'}

    def __init__(self, *args, **kwargs):
        """

        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update(
            {
                'class': 'form-select',
                'aria-label': 'Kategorie registrace',
                'placeholder': 'Zvolte kategorii'
            }
        )

    def clean(self):
        """
        Performs comprehensive validation: checks the user's age and gender
        against the category.

        Returns:
            The cleaned form data.

        Raises:
            ValidationError: If the user does not have a date of birth, does
            not meet the minimum or maximum age, or their gender does not
            match the category.
        """

        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        user = self.user

        if not category or not user:
            return cleaned_data
        if not user.birth_date:
            raise forms.ValidationError(
                "Uživatel nemá vyplněné datum narození."
            )
        
        today = date.today()
        age = today.year - user.birth_date.year - (
            (today.month, today.day) < 
            (user.birth_date.month, user.birth_date.day)
        )

        if category.min_age and age < category.min_age:
            raise forms.ValidationError(
                "Vašemu věku neodpovídá vybraná kategorie."
            )
        if category.max_age and age > category.max_age:
            raise forms.ValidationError(
                "Vašemu věku neodpovídá vybraná kategorie."
            )
        if category.gender != 'X' and category.gender != user.sex:
            raise forms.ValidationError(
                "Vaše pohlaví neodpovídá vybrané kategorii."
            )
        return cleaned_data
    
    def clean_category(self):
        """
        Verifies that the user has indeed selected a category.

        Returns:
            The selected category from validated_data.

        Raises:
            ValidationError: If the 'category' field was left empty.
        """

        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("Musíte vybrat kategorii.")
        return category
    