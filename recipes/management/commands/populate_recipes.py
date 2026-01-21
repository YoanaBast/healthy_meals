from django.core.management.base import BaseCommand
from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredient

class Command(BaseCommand):
    help = "Populate sample recipes using existing ingredients"

    def handle(self, *args, **kwargs):
        # Get ingredients by name
        olive_oil = Ingredient.objects.get(name='Olive Oil')
        cinnamon = Ingredient.objects.get(name='Cinnamon')
        sugar = Ingredient.objects.get(name='Sugar')
        butter = Ingredient.objects.get(name='Butter')
        flour = Ingredient.objects.get(name='Flour')
        milk = Ingredient.objects.get(name='Milk')
        egg = Ingredient.objects.get(name='Egg')

        # Recipe 1: Pancake
        pancake, _ = Recipe.objects.get_or_create(name='Pancake')
        RecipeIngredient.objects.get_or_create(recipe=pancake, ingredient=flour, quantity=100, unit='g')
        RecipeIngredient.objects.get_or_create(recipe=pancake, ingredient=milk, quantity=1, unit='cup')
        RecipeIngredient.objects.get_or_create(recipe=pancake, ingredient=egg, quantity=1, unit='pc')
        RecipeIngredient.objects.get_or_create(recipe=pancake, ingredient=sugar, quantity=10, unit='g')
        RecipeIngredient.objects.get_or_create(recipe=pancake, ingredient=butter, quantity=1, unit='tbsp')

        # Recipe 2: Cinnamon Sugar Toast
        toast, _ = Recipe.objects.get_or_create(name='Cinnamon Sugar Toast')
        RecipeIngredient.objects.get_or_create(recipe=toast, ingredient=butter, quantity=1, unit='tbsp')
        RecipeIngredient.objects.get_or_create(recipe=toast, ingredient=sugar, quantity=5, unit='g')
        RecipeIngredient.objects.get_or_create(recipe=toast, ingredient=cinnamon, quantity=1, unit='tsp')

        # Recipe 3: Buttered Olive Oil Egg
        egg_dish, _ = Recipe.objects.get_or_create(name='Buttered Olive Oil Egg')
        RecipeIngredient.objects.get_or_create(recipe=egg_dish, ingredient=egg, quantity=2, unit='pc')
        RecipeIngredient.objects.get_or_create(recipe=egg_dish, ingredient=olive_oil, quantity=1, unit='tbsp')
        RecipeIngredient.objects.get_or_create(recipe=egg_dish, ingredient=butter, quantity=1, unit='tbsp')

        self.stdout.write(self.style.SUCCESS("Sample recipes created successfully!"))
