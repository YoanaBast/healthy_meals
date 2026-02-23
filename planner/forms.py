from django import forms
from .models import UserFridge
from core.mixins import ErrorMessagesMixin

class UserFridgeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_error_messages(['quantity', 'unit'])

    class Meta:
        model = UserFridge
        exclude = ['user', 'ingredient']
