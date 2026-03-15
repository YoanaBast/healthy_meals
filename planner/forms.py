from django import forms
from .models import UserFridge
from core.mixins import ErrorMessagesMixin

class UserFridgeForm(ErrorMessagesMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_error_messages(['quantity', 'unit'])

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity < 0.01:
            raise forms.ValidationError('Quantity must be at least 0.01.')
        return quantity

    class Meta:
        model = UserFridge
        exclude = ['user', 'ingredient']
