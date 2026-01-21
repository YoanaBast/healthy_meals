from django.db import models

from ingredients.models import IngredientMeasurementUnit, Ingredient


# Create your models here.


class Recipe(models.Model):

    name = models.CharField(max_length=200)
    cooking_time = models.TimeField(null=True, blank=True)
    servings = models.PositiveIntegerField(default=1)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='recipes')


    @property
    def nutrients(self):

        """
        Returns a dict of total nutrients for the recipe.
        Scales each ingredient by its quantity and unit.
        """

        total = {}

        for ri in self.recipe_ingredients.all():
            ing = ri.ingredient
            qty = ri.quantity
            unit = ri.unit

            ing_totals = ing.total_nutrients(unit=unit)

            for nutrient, value in ing_totals.items():
                if value == 'Info not available':
                    continue
                total[nutrient] = total.get(nutrient, 0) + value

        # Ensure all nutrients appear
        all_nutrients = set().union(*(ri.ingredient.NUTRIENTS for ri in self.recipe_ingredients.all()))
        return {n: total.get(n, 'Info not available') for n in all_nutrients}


    @property
    def quantity_ingredients(self):
        ...




class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    quantity = models.FloatField()
    unit = models.CharField(max_length=10, choices=IngredientMeasurementUnit.MeasureUnits.choices)


    class Meta:
        unique_together = ('recipe', 'ingredient')
