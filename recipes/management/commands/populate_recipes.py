from django.core.management.base import BaseCommand
from ingredients.models import Ingredient, IngredientMeasurementUnit
from recipes.models import Recipe, RecipeIngredient

class Command(BaseCommand):
    help = "Populate sample recipes using existing ingredients"

    def handle(self, *args, **kwargs):
        # Fetch ingredients
        ingredients = {i.name: i for i in Ingredient.objects.filter(
            name__in=['Olive Oil', 'Cinnamon', 'Sugar', 'Butter', 'Flour', 'Milk', 'Egg']
        )}

        # Helper to create RecipeIngredient
        def add_ingredient(recipe, name, qty, unit_code):
            ing = ingredients[name]
            # Use unit choices from IngredientMeasurementUnit
            if unit_code not in dict(IngredientMeasurementUnit.MeasureUnits.choices):
                self.stdout.write(self.style.WARNING(f"Unit '{unit_code}' not in choices for {name}, defaulting to 'g'"))
                unit_code = 'g'
            RecipeIngredient.objects.update_or_create(
                recipe=recipe,
                ingredient=ing,
                defaults={'quantity': qty, 'unit': unit_code}
            )

        # Recipe 1: Pancake
        pancake, _ = Recipe.objects.get_or_create(name='Pancake')
        add_ingredient(pancake, 'Flour', 100, 'g')
        add_ingredient(pancake, 'Milk', 1, 'cup')
        add_ingredient(pancake, 'Egg', 1, 'pc')
        add_ingredient(pancake, 'Sugar', 10, 'g')
        add_ingredient(pancake, 'Butter', 1, 'tbsp')

        # Recipe 2: Cinnamon Sugar Toast
        toast, _ = Recipe.objects.get_or_create(name='Cinnamon Sugar Toast')
        add_ingredient(toast, 'Butter', 1, 'tbsp')
        add_ingredient(toast, 'Sugar', 5, 'g')
        add_ingredient(toast, 'Cinnamon', 1, 'tsp')

        # Recipe 3: Buttered Olive Oil Egg
        egg_dish, _ = Recipe.objects.get_or_create(name='Buttered Olive Oil Egg')
        add_ingredient(egg_dish, 'Egg', 2, 'pc')
        add_ingredient(egg_dish, 'Olive Oil', 1, 'tbsp')
        add_ingredient(egg_dish, 'Butter', 1, 'tbsp')

        self.stdout.write(self.style.SUCCESS("Sample recipes created successfully!"))
