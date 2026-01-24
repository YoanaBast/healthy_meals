import json
import os

from django.core.management.base import BaseCommand
from ingredients.management.nutrients import *
from ingredients.models import Ingredient, IngredientCategory, IngredientDietaryTag, IngredientMeasurementUnit

json_path = os.path.join(os.path.dirname(__file__), 'nutrients.json')

with open(json_path) as f:
    ingredients_data = json.load(f)

def create_categories():
    """Creates all categories if they don't already exist"""
    categories = [
        'Vegetable', 'Fruit', 'Dairy & Eggs', 'Meat', 'Grain', 'Spice',
        'Seafood', 'Butter & Oil', 'Nuts & Seeds', 'Legumes'
    ]
    for name in categories:
        IngredientCategory.objects.get_or_create(name=name)


def create_dietary_tags():
    """Creates all dietary tags if they don't already exist"""
    tags = ['Vegan', 'Vegetarian', 'Gluten-Free', 'Dairy-Free', 'Nut-Free', 'Sugar-Free']
    for name in tags:
        IngredientDietaryTag.objects.get_or_create(name=name)


def create_ingredient(
        name: str,
        category_name: str = None,
        dietary_tags: list = None,
        default_unit_code: str = 'g',
        base_quantity: float = 100,
        conversion_to_base: float = None,
        **nutrients
):
    """
    Creates or updates an ingredient with a default measurement unit.

    :param name: Ingredient name
    :param category_name: Category name
    :param dietary_tags: List of dietary tag names
    :param default_unit_code: Unit code, e.g., 'g', 'cup', 'tbsp'
    :param base_quantity: Quantity nutrients are based on in default unit
    :param conversion_to_base: How much this unit equals in base (grams)
    :param nutrients: dict of nutrient values, e.g., kcal=100, protein=5
    """
    category = IngredientCategory.objects.filter(name=category_name).first() if category_name else None

    defaults = {'category': category, 'base_quantity': base_quantity}
    # sanitize nutrients so None → 0
    cleaned_nutrients = {f'base_quantity_{k}': (v or 0) for k, v in nutrients.items()}
    defaults.update(cleaned_nutrients)
    ingredient, created = Ingredient.objects.update_or_create(
        name=name,
        defaults=defaults
    )

    if dietary_tags:
        existing_tags = IngredientDietaryTag.objects.filter(name__in=dietary_tags)
        ingredient.dietary_tag.add(*existing_tags)

    # determine conversion to base
    if conversion_to_base is None:
        conversion_to_base = base_quantity if default_unit_code in ['g', 'ml'] else 1

    # create or update default measurement unit
    IngredientMeasurementUnit.objects.update_or_create(
        ingredient=ingredient,
        unit=default_unit_code,
        defaults={'conversion_to_base': conversion_to_base}
    )

    ingredient.save()


class Command(BaseCommand):
    help = 'Populate ingredients with dummy data'

    def handle(self, *args, **kwargs):
        create_categories()
        create_dietary_tags()

        create_ingredient(
            'Egg',
            'Dairy & Eggs',
            ['Nut-Free', 'Sugar-Free', 'Gluten-Free', 'Vegetarian'],
            default_unit_code='pc',
            base_quantity=1,
            conversion_to_base=1,
            **egg_nutrients
        )

        create_ingredient(
            'Milk',
            'Dairy & Eggs',
            ['Nut-Free', 'Sugar-Free', 'Gluten-Free', 'Vegetarian'],
            default_unit_code='cup',
            base_quantity=1,
            conversion_to_base=240,  # 1 cup milk ≈ 240g
            **milk_nutrients
        )

        create_ingredient(
            'Flour',
            'Grain',
            ['Nut-Free', 'Sugar-Free', 'Vegan', 'Vegetarian', 'Dairy-Free'],
            default_unit_code='g',
            base_quantity=100,
            conversion_to_base=100,
            **flour_nutrients
        )

        create_ingredient(
            'Butter',
            'Butter & Oil',
            ['Nut-Free', 'Sugar-Free', 'Vegetarian', 'Gluten-Free'],
            default_unit_code='tbsp',
            base_quantity=1,
            conversion_to_base=14,  # 1 tbsp ≈ 14g
            **butter_nutrients
        )

        create_ingredient(
            'Sugar',
            'Spice',
            ['Vegan', 'Vegetarian', 'Gluten-Free', 'Dairy-Free', 'Nut-Free'],
            default_unit_code='g',
            base_quantity=100,
            conversion_to_base=100,
            **sugar_nutrients
        )

        create_ingredient(
            'Cinnamon',
            'Spice',
            ['Vegan', 'Vegetarian', 'Gluten-Free', 'Dairy-Free', 'Nut-Free', 'Sugar-Free'],
            default_unit_code='tsp',
            base_quantity=1,
            conversion_to_base=2.6,  # 1 tsp cinnamon ≈ 2.6g
            **cinnamon_nutrients
        )

        create_ingredient(
            'Olive Oil',
            'Butter & Oil',
            ['Vegan', 'Vegetarian', 'Gluten-Free', 'Dairy-Free', 'Nut-Free', 'Sugar-Free'],
            default_unit_code='tbsp',
            base_quantity=1,
            conversion_to_base=13.5,  # 1 tbsp ≈ 13.5g
            **olive_oil_nutrients
        )

        self.stdout.write(self.style.SUCCESS('Dummy ingredients populated successfully!'))
