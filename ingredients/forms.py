from django import forms
from .models import Ingredient, IngredientDietaryTag

NUTRIENTS = [
    'kcal', 'protein', 'carbs', 'fat', 'fiber', 'sugar', 'salt', 'cholesterol',
    'vitamin_a', 'vitamin_c', 'vitamin_d', 'vitamin_e', 'vitamin_k',
    'vitamin_b1', 'vitamin_b2', 'vitamin_b3', 'vitamin_b6', 'vitamin_b12',
    'folate', 'calcium', 'iron', 'magnesium', 'potassium', 'zinc'
]


class IngredientFormBase(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = (
                ['name', 'category', 'dietary_tag', 'base_quantity', 'default_unit'] +
                [f'base_quantity_{n}' for n in NUTRIENTS]
        )
        #  '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'dietary_tag': forms.CheckboxSelectMultiple(),  # multiple choice
            'default_unit': forms.Select(attrs={'class': 'form-select'}),
            'base_quantity': forms.NumberInput(attrs={'class': 'form-input', 'value': 100, 'min': 0}, ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['dietary_tag'].required = False  # making optional

        for nutrient in NUTRIENTS:
            field = f'base_quantity_{nutrient}'
            self.fields[field].label = nutrient.replace('_', ' ').title()
            self.fields[field].required = False
            self.fields[field].initial = 0
            self.fields[field].widget = forms.NumberInput(
                attrs={'class': 'form-input', 'value': 0, 'step': 'any',  'min': 0}  # allows float
            )





class IngredientAddForm(IngredientFormBase):
    ...


class IngredientEditForm(IngredientFormBase):
    ...