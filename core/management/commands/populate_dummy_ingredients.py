import json
from pathlib import Path
from django.core.management.base import BaseCommand
from ingredients.models import (
    Ingredient,
    IngredientCategory,
    IngredientDietaryTag,
    IngredientMeasurementUnit
)


class Command(BaseCommand):
    help = 'Populate ingredients from dummy_ingredients.json'

    def handle(self, *args, **kwargs):
        json_path = Path(__file__).resolve().parent.parent / 'dummy_data' / 'dummy_ingredients.json'
        self.stdout.write(f"DEBUG: Looking for JSON at {json_path}")

        if not json_path.exists():
            self.stdout.write(self.style.ERROR("ERROR: File not found!"))
            return

        with open(json_path, 'r') as f:
            data = json.load(f)

        # Create categories and dietary tags from JSON
        self.create_categories(data.get('categories', []))
        self.create_dietary_tags(data.get('dietary_tags', []))

        # Process ingredients
        ingredients_data = data.get('ingredients', {})
        for name, info in ingredients_data.items():
            self.stdout.write(f"\n>>> PROCESSING: {name}")
            self.process_ingredient(name, info)

        self.stdout.write(self.style.SUCCESS('\nFinished populating ingredients!'))

    def create_categories(self, categories):
        for name in categories:
            _, created = IngredientCategory.objects.get_or_create(name=name)
            if created:
                self.stdout.write(f"DEBUG: Created Category: {name}")

    def create_dietary_tags(self, tags):
        for name in tags:
            _, created = IngredientDietaryTag.objects.get_or_create(name=name)
            if created:
                self.stdout.write(f"DEBUG: Created Tag: {name}")

    def process_ingredient(self, name, data):
        # Category
        category = IngredientCategory.objects.filter(name=data.get('category')).first()

        # Base quantity and unit
        base_qty = data.get('base_quantity', 100)
        defaults = {
            'category': category,
            'base_quantity': base_qty,
            'default_unit': data.get('primary_unit', 'g'),
        }

        # Nutrients
        for nutrient in Ingredient.NUTRIENTS:
            val = data.get(nutrient, 0)
            defaults[f'base_quantity_{nutrient}'] = val or 0

        ingredient, _ = Ingredient.objects.update_or_create(name=name, defaults=defaults)

        # Dietary tags
        if 'dietary_tags' in data:
            tags = IngredientDietaryTag.objects.filter(name__in=data['dietary_tags'])
            ingredient.dietary_tag.set(tags)

        # Measurement units
        for unit_info in data.get('units', []):
            unit_code = unit_info.get('unit')
            conversion = unit_info.get('conversion_to_base', 1.0)

            # Simple fallback for common units
            if conversion is None:
                conversion = 1.0 if unit_code != 'cup' else 240.0

            IngredientMeasurementUnit.objects.update_or_create(
                ingredient=ingredient,
                unit=unit_code,
                defaults={'conversion_to_base': conversion}
            )
            self.stdout.write(f"DEBUG: Set unit {unit_code} for {name} → {conversion}g")
