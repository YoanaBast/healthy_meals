from django.db import models

from ingredients.models import Ingredient


# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=200)
    cooking_time = models.TimeField(null=True, blank=True)
    servings = models.PositiveIntegerField(default=1)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='recipes')

    @property
    def nutrients(self):
        """
        Returns a dict of total nutrients for the recipe using Ingredient.total_nutrients
        """
        total = {}

        for ri in self.recipe_ingredients.all():
            ing = ri.ingredient
            qty = ri.quantity
            ing_totals = ing.total_nutrients  # existing property

            for nutrient, value in ing_totals.items():
                if value == 'Info not available':
                    continue
                # Scale by quantity in the recipe
                total[nutrient] = total.get(nutrient, 0) + ing.total_nutrient(nutrient, qty)

        # Fill missing nutrients with 'Info not available'
        all_nutrients = set().union(*(ri.ingredient.total_nutrients.keys() for ri in self.recipe_ingredients.all()))
        return {n: total.get(n, 'Info not available') for n in all_nutrients}

    @property
    def quantity_ingredients(self):
        ...



class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    quantity = models.FloatField()
    unit = models.CharField(max_length=10, choices=Ingredient.MeasureUnits.choices)


    class Meta:
        unique_together = ('recipe', 'ingredient')
