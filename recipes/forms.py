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
        self.fields['unit'].queryset = IngredientMeasurementUnit.objects.none()

        if self.is_bound:
            ingredient_id = self.data.get(self.add_prefix('ingredient'))
            if ingredient_id:
                try:
                    ingredient = Ingredient.objects.get(pk=int(ingredient_id))
                    self.fields['unit'].queryset = ingredient.measurement_units.values_list('unit', flat=True)
                except:
                    pass
        elif self.instance.pk and self.instance.ingredient:
            self.fields['unit'].queryset = self.instance.ingredient.measurement_units.values_list('unit', flat=True)


RecipeIngredientFormSet = inlineformset_factory(
    Recipe, RecipeIngredient, form=RecipeIngredientForm,
    extra=3, can_delete=True  # extra=3 gives 3 blank rows to start, user can fill multiple ingredients
)