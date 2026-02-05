import json
from pathlib import Path
from django.core.management.base import BaseCommand
from recipes.models import Recipe, RecipeIngredient, RecipeCategory
from ingredients.models import Ingredient, IngredientMeasurementUnit


class Command(BaseCommand):
    help = 'Populate dummy recipes using existing ingredients from JSON'

    def handle(self, *args, **kwargs):
        json_path = Path(__file__).resolve().parent.parent / 'dummy_data' / 'dummy_recipes.json'
        self.stdout.write(f"DEBUG: Looking for JSON at {json_path}")

        if not json_path.exists():
            self.stdout.write(self.style.ERROR("ERROR: File not found!"))
            return

        with open(json_path, 'r') as f:
            data = json.load(f)

        # Create categories dynamically
        for cat_name in data.get('categories', []):
            _, created = RecipeCategory.objects.get_or_create(name=cat_name)
            if created:
                self.stdout.write(f"DEBUG: Created Recipe Category: {cat_name}")

        # Process recipes
        for recipe_name, info in data.get('recipes', {}).items():
            cat_name = info.get('category')
            category = RecipeCategory.objects.filter(name=cat_name).first() if cat_name else None

            recipe, _ = Recipe.objects.get_or_create(
                name=recipe_name,
                defaults={
                    'category': category,
                    'cooking_time': info.get('cooking_time'),
                    'servings': info.get('servings', 1)
                }
            )
            self.stdout.write(f"\n>>> PROCESSING RECIPE: {recipe_name}")

            for ing_info in info.get('ingredients', []):
                ing_name = ing_info['name']
                qty = ing_info['quantity']
                unit = ing_info['unit']

                # Only use existing ingredients
                ingredient = Ingredient.objects.filter(name=ing_name).first()
                if not ingredient:
                    self.stdout.write(self.style.WARNING(f"Skipping missing ingredient: {ing_name}"))
                    continue

                # Validate unit
                valid_units = [u.unit for u in ingredient.measurement_units.all()]
                if unit not in valid_units:
                    self.stdout.write(self.style.WARNING(
                        f"Unit '{unit}' not found for {ing_name}, defaulting to '{ingredient.default_unit}'"
                    ))
                    unit = ingredient.default_unit

                # Create/update RecipeIngredient
                ri, _ = RecipeIngredient.objects.update_or_create(
                    recipe=recipe,
                    ingredient=ingredient,
                    defaults={'quantity': qty, 'unit': unit}
                )

                self.stdout.write(f"DEBUG: Added {qty} {unit} of {ing_name} to {recipe_name}")

        self.stdout.write(self.style.SUCCESS("\nAll recipes populated successfully!"))
