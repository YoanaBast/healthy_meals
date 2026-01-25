from django.core.management.base import BaseCommand
from ingredients.models import Ingredient, IngredientMeasurementUnit
from recipes.models import Recipe, RecipeIngredient


class Command(BaseCommand):
    help = "Populate sample recipes using existing ingredients (No Sugar Version)"

    def handle(self, *args, **kwargs):
        # Fetching only the ingredients we know we have
        # Removed 'Sugar' from this list
        ingredients = {i.name: i for i in Ingredient.objects.filter(
            name__in=['Olive Oil', 'Cinnamon', 'Butter', 'Flour', 'Milk', 'Egg']
        )}

        def add_ingredient(recipe, name, qty, unit_code):
            # Using .get() to prevent crashing if an ingredient is missing
            ing = ingredients.get(name)

            if not ing:
                self.stdout.write(self.style.ERROR(f"DEBUG: Skipping {name} - not found in database!"))
                return

            if unit_code not in dict(IngredientMeasurementUnit.MeasureUnits.choices):
                self.stdout.write(self.style.WARNING(f"Unit '{unit_code}' not valid for {name}, defaulting to 'g'"))
                unit_code = 'g'

            # Create the Recipe-Ingredient link
            ri, _ = RecipeIngredient.objects.update_or_create(
                recipe=recipe,
                ingredient=ing,
                defaults={'quantity': qty, 'unit': unit_code}
            )

            # Debugging the Calories for this specific addition
            try:
                unit_obj = ing.measurement_units.get(unit=unit_code)
                nutrients = ing.get_nutrients_dict(unit_obj, qty)
                kcal = nutrients.get('kcal', 0)
            except IngredientMeasurementUnit.DoesNotExist:
                kcal = 0

            print(f"DEBUG: Added {qty} {unit_code} of {name} to {recipe.name} → {kcal:.1f} kcal")

        # --- Recipe 1: Savory Pancake (No Sugar) ---
        pancake, _ = Recipe.objects.get_or_create(name='Pancake')
        add_ingredient(pancake, 'Flour', 100, 'g')
        add_ingredient(pancake, 'Milk', 1, 'cup')
        add_ingredient(pancake, 'Egg', 1, 'pc')
        add_ingredient(pancake, 'Butter', 1, 'tbsp')

        # --- Recipe 2: Cinnamon Butter Toast (No Sugar) ---
        # Note: Usually needs sugar, but we are omitting per request
        toast, _ = Recipe.objects.get_or_create(name='Cinnamon Butter Toast')
        add_ingredient(toast, 'Butter', 1, 'tbsp')
        add_ingredient(toast, 'Cinnamon', 1, 'tsp')

        # --- Recipe 3: Buttered Olive Oil Egg ---
        egg_dish, _ = Recipe.objects.get_or_create(name='Buttered Olive Oil Egg')
        add_ingredient(egg_dish, 'Egg', 2, 'pc')
        add_ingredient(egg_dish, 'Olive Oil', 1, 'tbsp')
        add_ingredient(egg_dish, 'Butter', 1, 'tbsp')

        self.stdout.write(self.style.SUCCESS("\nSample recipes created successfully!"))