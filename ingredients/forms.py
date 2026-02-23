from django import forms

from core.constants import NUTRIENTS
from .models import Ingredient, IngredientMeasurementUnit



class IngredientFormBase(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = (
            ['name', 'category', 'dietary_tag', 'base_quantity', 'default_unit'] +
            [f'base_quantity_{n}' for n in NUTRIENTS]
        )

        widgets = {
            'ingredient': forms.Select(attrs={
                'onchange': 'updateUnit(this)'  # JS behaviour, stays here
            }),
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'dietary_tag': forms.CheckboxSelectMultiple(attrs={'class': 'dietary-tags'}),
            'default_unit': forms.Select(attrs={'class': 'form-select half-width'}),
            'base_quantity': forms.NumberInput(attrs={'class': 'form-input half-width', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['dietary_tag'].required = False

        for nutrient in NUTRIENTS:
            field = f'base_quantity_{nutrient}'
            self.fields[field].label = nutrient.replace('_', ' ').title()
            self.fields[field].required = False
            self.fields[field].initial = 0
            self.fields[field].widget = forms.NumberInput(
                attrs={'class': 'form-input nutrient-input', 'step': 'any', 'min': 0}
            )

        self.fields['base_quantity_kcal'].help_text = 'Calories per base quantity.'
        self.fields['base_quantity_protein'].help_text = 'In grams.'
        self.fields['base_quantity_fat'].help_text = 'Total fat in grams.'

class IngredientAddForm(IngredientFormBase):
    def save(self, commit=True):
        ingredient = super().save(commit=commit)
        if commit:
            IngredientMeasurementUnit.objects.get_or_create(
                ingredient=ingredient,
                unit=ingredient.default_unit,
                conversion_to_base=ingredient.base_quantity
            )
        return ingredient


class IngredientEditForm(IngredientFormBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['base_quantity'].widget.attrs['readonly'] = True
        self.fields['base_quantity'].help_text = 'Base quantity cannot be changed after creation as it affects nutrient calculations.'