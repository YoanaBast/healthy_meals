import json
from pathlib import Path
from django.core.management.base import BaseCommand
from ingredients.models import (
    Ingredient,
    IngredientCategory,
    IngredientDietaryTag,
    IngredientMeasurementUnit,
    MeasurementUnit
)


class Command(BaseCommand):
    help = 'Populate ingredients and units from JSON'

    def handle(self, *args, **kwargs):
        json_path = Path(__file__).resolve().parent.parent / 'dummy_data' / 'dummy_ingredients.json'
        self.stdout.write(f"DEBUG: Looking for JSON at {json_path}")

        if not json_path.exists():
            self.stdout.write(self.style.ERROR("ERROR: File not found!"))
            return

        with open(json_path, 'r') as f:
            data = json.load(f)

        # 1️⃣ Create units table from JSON
        self.create_units(data.get('units', {}))

        # 2️⃣ Create categories and dietary tags
        self.create_categories(data.get('categories', []))
        self.create_dietary_tags(data.get('dietary_tags', []))

        # 3️⃣ Process ingredients and link units
        ingredients_data = data.get('ingredients', {})
        for name, info in ingredients_data.items():
            self.stdout.write(f"\n>>> PROCESSING: {name}")
            self.process_ingredient(name, info, data.get('units', {}))

        self.stdout.write(self.style.SUCCESS('\nFinished populating ingredients!'))

    def create_units(self, units_dict):
        for code, names in units_dict.items():
            unit, created = MeasurementUnit.objects.get_or_create(
                code=code,
                defaults={'name_singular': names.get('singular', code), 'name_plural': names.get('plural', code)}
            )
            if created:
                self.stdout.write(f"DEBUG: Created MeasurementUnit: {code} → {names.get('singular')}")

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

    def process_ingredient(self, name, data, units_dict):
        # Category
        category = IngredientCategory.objects.filter(name=data.get('category')).first()

        # Base quantity and default unit
        base_qty = data.get('base_quantity', 100)
        unit_code = data.get('primary_unit', 'g')
        default_unit_obj = MeasurementUnit.objects.get(code=unit_code)
        defaults = {
            'category': category,
            'base_quantity': base_qty,
            'default_unit': default_unit_obj,  # <-- assign object
        }

        # Nutrients
        for nutrient in Ingredient.NUTRIENTS:
            val = data.get(nutrient, 0)
            defaults[f'base_quantity_{nutrient}'] = val or 0

        # Create or update ingredient
        ingredient, _ = Ingredient.objects.update_or_create(name=name, defaults=defaults)

        # Dietary tags
        if 'dietary_tags' in data:
            tags = IngredientDietaryTag.objects.filter(name__in=data['dietary_tags'])
            ingredient.dietary_tag.set(tags)

        # Measurement units (junction table)
        for unit_info in data.get('units', []):
            code = unit_info.get('unit')
            conversion = unit_info.get('conversion_to_base', 1.0)

            # Get the MeasurementUnit object
            unit_obj = MeasurementUnit.objects.get(code=code)

            IngredientMeasurementUnit.objects.update_or_create(
                ingredient=ingredient,
                unit=unit_obj,  # <-- assign object, not string
                defaults={'conversion_to_base': conversion}
            )
            self.stdout.write(f"DEBUG: Linked {ingredient.name} → {unit_obj.code} ({conversion})")
