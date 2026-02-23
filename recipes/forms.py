from datetime import time

from django import forms
from django.forms import inlineformset_factory

from .models import Recipe, RecipeIngredient, RecipeCategory
from ingredients.models import Ingredient, IngredientMeasurementUnit


class RecipeFormAdmin(forms.ModelForm):
    """
    Changes the input/edit option for the cooking time — default was time not duration.
    """
    class Meta:
        model = Recipe
        fields = '__all__'
        widgets = {
            'cooking_time': forms.TimeInput(format='%H:%M'),
        }


class RecipeForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=RecipeCategory.objects.all().order_by('name'),
        required=False
    )

    hours = forms.IntegerField(
        min_value=0, max_value=23, required=True, label="Hours", initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-input small-width', 'min': 0}),
        error_messages={
            'required': 'Please enter the cooking hours.',
            'min_value': 'Hours cannot be negative.',
            'max_value': 'Hours cannot exceed 23.',
            'invalid': 'Enter a whole number for hours.',
        }
    )
    minutes = forms.IntegerField(
        min_value=0, max_value=59, required=True, label="Minutes", initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-input small-width', 'min': 0}),
        error_messages={
            'required': 'Please enter the cooking minutes.',
            'max_value': 'Minutes cannot exceed 59.',
            'invalid': 'Enter a whole number for minutes.',
        }
    )
    servings = forms.IntegerField(
        min_value=1, initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-input small-width', 'min': 1, 'step': 1}),
        error_messages={
            'required': 'Please enter the number of servings.',
            'min_value': 'Servings must be at least 1.',
            'invalid': 'Enter a whole number for servings.',
        }
    )

    class Meta:
        model = Recipe
        exclude = ['cooking_time', 'ingredients', 'favourited_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.cooking_time:
            self.fields['hours'].initial = self.instance.cooking_time.hour
            self.fields['minutes'].initial = self.instance.cooking_time.minute

    def clean(self):
        cleaned_data = super().clean()
        h = cleaned_data.get('hours', 0)
        m = cleaned_data.get('minutes', 0)
        cleaned_data['cooking_time'] = f"{h:02d}:{m:02d}:00"
        return cleaned_data

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')
        if servings is None or servings < 1:
            raise forms.ValidationError("Servings must be at least 1.")
        return servings

    def save(self, commit=True):
        instance = super().save(commit=False)
        h = self.cleaned_data.get('hours', 0)
        m = self.cleaned_data.get('minutes', 0)
        instance.cooking_time = time(hour=h, minute=m)
        instance.category = self.cleaned_data.get('category')
        if commit:
            instance.save()
        return instance


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        exclude = ['recipe']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['unit'].queryset = IngredientMeasurementUnit.objects.none()

        if self.is_bound:
            ingredient_id = self.data.get(self.add_prefix('ingredient'))
            if ingredient_id:
                try:
                    self.fields['unit'].queryset = IngredientMeasurementUnit.objects.filter(
                        ingredient_id=int(ingredient_id)
                    )
                except (ValueError, TypeError):
                    pass

        elif self.instance.pk and self.instance.ingredient:
            self.fields['unit'].queryset = IngredientMeasurementUnit.objects.filter(
                ingredient=self.instance.ingredient
            )

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity is not None and quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return quantity


RecipeIngredientFormSet = inlineformset_factory(
    Recipe, RecipeIngredient,
    form=RecipeIngredientForm,
    extra=0,
    can_delete=True
)