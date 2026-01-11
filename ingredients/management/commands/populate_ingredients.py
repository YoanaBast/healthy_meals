from django.core.management.base import BaseCommand
from ingredients.dummy_data.nutrients import *
from ingredients.models import Ingredient, IngredientCategory, IngredientDietaryTag


def create_categories():
    """
    creates all categories in the list if they don't already exist
    :return: None
    """
    categories = ['Vegetable', 'Fruit', 'Dairy & Eggs', 'Meat', 'Grain', 'Spice', 'Seafood', 'Butter & Oil', 'Nuts & Seeds', 'Legumes', ]
    for name in categories:
        IngredientCategory.objects.get_or_create(name=name)


def create_dietary_tags():
    """
    creates all tags in the list if they don't already exist
    :return: None
    """
    tags = ['Vegan', 'Vegetarian', 'Gluten-Free', 'Dairy-Free', 'Nut-Free', 'Sugar-Free']
    for name in tags:
        IngredientDietaryTag.objects.get_or_create(name=name)


def create_ingredient(
    name,
    category_name,
    dietary_tags=None,
    min_measure_unit='g',
    base_quantity=100,
    **nutrients
):
    """
    - creates an ingredient
    - category is handled at the top as the Ingredient model has a ForeignKey to IngredientCategory, so when we create an ingredient, Django expects a category object or None.
    - get ot create - search by name and if it does not exist, it is created with teh default params
    - each given dietary tag is added

    :param name: 'Egg'
    :param category_name: 'Dairy & Eggs'
    :param dietary_tags: ['Nut-Free', 'Sugar-Free']
    :param min_measure_unit: 'pc'
    :param base_quantity: 1
    :param nutrients: {...}
    :return: None
    """
    category = IngredientCategory.objects.filter(name=category_name).first() if category_name else None

    defaults = {'category': category, 'min_measure_unit': min_measure_unit, 'base_quantity': base_quantity}
    defaults.update({f'base_quantity_{k}': v for k, v in nutrients.items()})

    ingredient, created = Ingredient.objects.update_or_create(
        name=name,
        defaults=defaults
    )

    if dietary_tags:
        existing_tags = IngredientDietaryTag.objects.filter(name__in=dietary_tags)
        ingredient.dietary_tag.add(*existing_tags)

    ingredient.save()



class Command(BaseCommand):
    help = 'Populate ingredients with dummy data'

    def handle(self, *args, **kwargs):
        create_categories()
        create_dietary_tags()

        create_ingredient('Egg',
                          'Dairy & Eggs',
                          ['Nut-Free', 'Sugar-Free', 'Gluten-Free', 'Vegetarian'],
                          'pc',
                          1,
                          **egg_nutrients)

        create_ingredient('Milk',
                          'Dairy & Eggs',
                          ['Nut-Free', 'Sugar-Free', 'Gluten-Free', 'Vegetarian'],
                          'cup',
                          1,
                          **milk_nutrients)

        create_ingredient('Flour',
                          'Grain',
                          ['Nut-Free', 'Sugar-Free', 'Vegan', 'Vegetarian', 'Dairy-Free'],
                          'g',
                          100,
                          **flour_nutrients)

        create_ingredient('Butter',
                          'Butter & Oil',
                          ['Nut-Free', 'Sugar-Free', 'Vegetarian', 'Gluten-Free'],
                          'tbsp',
                          1,
                          **butter_nutrients)

        create_ingredient('Sugar',
                          'Spice',
                          ['Vegan', 'Vegetarian', 'Gluten-Free', 'Dairy-Free', 'Nut-Free'],
                          'g',
                          100,
                          **sugar_nutrients)

        create_ingredient('Cinnamon',
                          'Spice',
                          ['Vegan', 'Vegetarian', 'Gluten-Free', 'Dairy-Free', 'Nut-Free', 'Sugar-Free'],
                          'tsp',
                          1,
                          **cinnamon_nutrients)

        create_ingredient('Olive Oil',
                          'Butter & Oil',
                          ['Vegan', 'Vegetarian', 'Gluten-Free', 'Dairy-Free', 'Nut-Free', 'Sugar-Free'],
                          'tbsp',
                          1,
                          **olive_oil_nutrients)
        self.stdout.write(self.style.SUCCESS('Dummy ingredients populated successfully!'))
