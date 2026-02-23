import json
from pathlib import Path
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ingredients.models import (
    Ingredient, IngredientCategory, IngredientDietaryTag,
    IngredientMeasurementUnit, MeasurementUnit
)
from planner.models import UserFridge
from recipes.models import Recipe, RecipeIngredient, RecipeCategory


class Command(BaseCommand):
    help = 'Populate all dummy data from a single JSON file'

    def handle(self, *args, **kwargs):
        json_path = Path(__file__).resolve().parent.parent / 'dummy_data' / 'dummy_data.json'

        if not json_path.exists():
            self.stdout.write(self.style.ERROR(f"File not found: {json_path}"))
            return

        with open(json_path, 'r') as f:
            data = json.load(f)

        self.create_units(data.get('units', {}))
        self.create_ingredient_categories(data['categories']['ingredient'])
        self.create_recipe_categories(data['categories']['recipe'])
        self.create_dietary_tags(data.get('dietary_tags', []))
        self.create_ingredients(data.get('ingredients', {}))
        self.create_fridge(data.get('fridge_items', []))
        self.create_recipes(data.get('recipes', {}))

        self.stdout.write(self.style.SUCCESS('Done! All dummy data populated.'))

    def create_units(self, units_dict):
        for code, names in units_dict.items():
            _, created = MeasurementUnit.objects.get_or_create(
                code=code,
                defaults={'name_singular': names['singular'], 'name_plural': names['plural']}
            )
            if created:
                self.stdout.write(f"  Unit: {code}")

    def create_ingredient_categories(self, categories):
        for name in categories:
            _, created = IngredientCategory.objects.get_or_create(name=name)
            if created:
                self.stdout.write(f"  Ingredient category: {name}")

    def create_recipe_categories(self, categories):
        for name in categories:
            _, created = RecipeCategory.objects.get_or_create(name=name)
            if created:
                self.stdout.write(f"  Recipe category: {name}")

    def create_dietary_tags(self, tags):
        for name in tags:
            _, created = IngredientDietaryTag.objects.get_or_create(name=name)
            if created:
                self.stdout.write(f"  Dietary tag: {name}")

    def create_ingredients(self, ingredients_dict):
        for name, info in ingredients_dict.items():
            category = IngredientCategory.objects.filter(name=info.get('category')).first()
            default_unit = MeasurementUnit.objects.filter(code=info.get('primary_unit')).first()

            defaults = {
                'category': category,
                'base_quantity': info.get('base_quantity', 100),
                'default_unit': default_unit,
            }
            for nutrient in Ingredient.NUTRIENTS:
                defaults[f'base_quantity_{nutrient}'] = info.get(nutrient, 0) or 0

            ingredient, _ = Ingredient.objects.update_or_create(name=name, defaults=defaults)

            if 'dietary_tags' in info:
                tags = IngredientDietaryTag.objects.filter(name__in=info['dietary_tags'])
                ingredient.dietary_tag.set(tags)

            for unit_info in info.get('units', []):
                unit_obj = MeasurementUnit.objects.filter(code=unit_info['unit']).first()
                if unit_obj:
                    IngredientMeasurementUnit.objects.update_or_create(
                        ingredient=ingredient,
                        unit=unit_obj,
                        defaults={'conversion_to_base': unit_info['conversion_to_base']}
                    )

            self.stdout.write(f"  Ingredient: {name}")

    def create_fridge(self, fridge_items):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username="default",
            defaults={"is_superuser": True, "is_staff": True}
        )
        if created:
            user.set_password("defaultpassword")
            user.save()
            self.stdout.write("  Created default user")

        for item in fridge_items:
            ingredient = Ingredient.objects.filter(name=item['name']).first()
            if not ingredient:
                self.stdout.write(self.style.WARNING(f"  Skipping fridge item — ingredient not found: {item['name']}"))
                continue

            unit = MeasurementUnit.objects.filter(code=item['unit']).first() or ingredient.default_unit

            UserFridge.objects.update_or_create(
                user=user,
                ingredient=ingredient,
                defaults={'quantity': item['quantity'], 'unit': unit}
            )
            self.stdout.write(f"  Fridge: {item['quantity']} {item['unit']} of {item['name']}")

    def create_recipes(self, recipes_dict):
        for name, info in recipes_dict.items():
            category = RecipeCategory.objects.filter(name=info.get('category')).first()

            recipe, _ = Recipe.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'cooking_time': info.get('cooking_time'),
                    'servings': info.get('servings', 1),
                    'instructions': info.get('instructions', ''),
                }
            )

            for ing_info in info.get('ingredients', []):
                ingredient = Ingredient.objects.filter(name=ing_info['name']).first()
                if not ingredient:
                    self.stdout.write(self.style.WARNING(f"  Skipping — ingredient not found: {ing_info['name']}"))
                    continue

                unit_obj = ingredient.measurement_units.filter(unit__code=ing_info['unit']).first()
                if not unit_obj:
                    self.stdout.write(self.style.WARNING(f"  Skipping — unit '{ing_info['unit']}' not found for {ing_info['name']}"))
                    continue

                RecipeIngredient.objects.update_or_create(
                    recipe=recipe,
                    ingredient=ingredient,
                    defaults={'quantity': ing_info['quantity'], 'unit': unit_obj}
                )

            self.stdout.write(f"  Recipe: {name}")