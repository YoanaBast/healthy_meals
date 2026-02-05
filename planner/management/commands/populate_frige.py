import json
import os
from django.core.management.base import BaseCommand
from planner.models import (
    Ingredient,
    IngredientCategory,
    IngredientDietaryTag,
    IngredientMeasurementUnit
)


class Command(BaseCommand):
    help = 'Populate ingredients using nutrients.json with debug prints'

    def handle(self, *args, **kwargs):
        # 1. Load the JSON data
        json_path = os.path.join(os.path.dirname(__file__), 'nutrients.json')

        self.stdout.write(f"DEBUG: Looking for JSON at {json_path}")

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"ERROR: File not found!"))
            return

        with open(json_path, 'r') as f:
            ingredients_data = json.load(f)

        self.stdout.write(f"DEBUG: Successfully loaded {len(ingredients_data)} ingredients from JSON.")

        # 2. Setup Categories and Tags
        self.create_categories()
        self.create_dietary_tags()

        # 3. Process each ingredient
        for name, data in ingredients_data.items():
            self.stdout.write(f"\n>>> PROCESSING: {name}")
            self.process_ingredient(name, data)

        self.stdout.write(self.style.SUCCESS('\nFinished populating ingredients!'))

    def create_categories(self):
        categories = [
            'Vegetable', 'Fruit', 'Dairy & Eggs', 'Meat', 'Grain', 'Spice',
            'Seafood', 'Butter & Oil', 'Nuts & Seeds', 'Legumes'
        ]
        for name in categories:
            _, created = IngredientCategory.objects.get_or_create(name=name)
            if created: print(f"DEBUG: Created Category: {name}")

    def create_dietary_tags(self):
        tags = ['Vegan', 'Vegetarian', 'Gluten-Free', 'Dairy-Free', 'Nut-Free', 'Sugar-Free']
        for name in tags:
            _, created = IngredientDietaryTag.objects.get_or_create(name=name)
            if created: print(f"DEBUG: Created Tag: {name}")

    def process_ingredient(self, name, data):
        # Find Category
        cat_name = data.get('category')
        category = IngredientCategory.objects.filter(name=cat_name).first()

        # Nutrients usually defined per 100g
        base_qty = data.get('base_quantity', 100)

        print(f"DEBUG: {name} base_quantity set to {base_qty}")

        defaults = {
            'category': category,
            'base_quantity': base_qty,
            'default_unit': data.get('primary_unit', 'g'),
        }

        # Map JSON nutrients to model fields
        for nutrient in Ingredient.NUTRIENTS:
            val = data.get(nutrient, 0)
            defaults[f'base_quantity_{nutrient}'] = val if val is not None else 0

        print(f"DEBUG: Kcal for {name} in JSON: {data.get('kcal')}")

        # Create/Update Ingredient
        ingredient, created = Ingredient.objects.update_or_create(
            name=name,
            defaults=defaults
        )

        # Tags
        if 'dietary_tags' in data:
            tags = IngredientDietaryTag.objects.filter(name__in=data['dietary_tags'])
            ingredient.dietary_tag.add(*tags)

        # Units - THE FIX IS HERE
        units_to_create = data.get('units', [])
        for unit_info in units_to_create:
            unit_code = unit_info.get('unit')
            # conversion = weight of 1 unit in grams
            conversion = unit_info.get('conversion_to_base')

            # Hard-coded safety fallbacks
            if conversion is None:
                if unit_code == 'g':
                    conversion = 1.0
                elif unit_code == 'cup':
                    conversion = 240.0
                else:
                    conversion = 1.0

            print(f"DEBUG: Setting Unit [{unit_code}] with Conversion Factor: {conversion}")

            IngredientMeasurementUnit.objects.update_or_create(
                ingredient=ingredient,
                unit=unit_code,
                defaults={'conversion_to_base': conversion}
            )