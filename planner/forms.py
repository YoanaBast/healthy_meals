from django import forms
from .models import UserFridge
from core.mixins import ErrorMessagesMixin

class UserFridgeForm(ErrorMessagesMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_error_messages(['quantity', 'unit'])

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity <= 0:
            raise forms.ValidationError('Quantity must be greater than 0.')
        return quantity

    class Meta:
        model = UserFridge
        exclude = ['user', 'ingredient']
