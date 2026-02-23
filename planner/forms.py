from django import forms
from .models import UserFridge

class UserFridgeForm(forms.ModelForm):
    class Meta:
        model = UserFridge
        exclude = ['user', 'ingredient']
