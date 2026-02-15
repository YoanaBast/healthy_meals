from django import forms
from django.forms import inlineformset_factory

from .models import Recipe, RecipeIngredient, RecipeCategory
from ingredients.models import Ingredient, IngredientMeasurementUnit


class RecipeFormAdmin(forms.ModelForm):
    """
    this changes the input/eedit option for the cooking time, the default was time and not duration
    """
    class Meta:
        model = Recipe
        fields = '__all__'
        widgets = {
            'cooking_time': forms.TimeInput(format='%H:%M'),  # HH:MM
        }

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'category', 'cooking_time', 'servings', 'instructions']

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Default empty
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
