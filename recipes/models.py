from django.db import models

from ingredients.models import IngredientMeasurementUnit, Ingredient


# Create your models here.

class RecipeCategory(models.Model):

    """
    INGREDIENT CATEGORY
    ex: Vegetables
    """

    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name




class Recipe(models.Model):

    name = models.CharField(max_length=200)
    cooking_time = models.TimeField(null=True, blank=True)
    servings = models.PositiveIntegerField(default=1)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='recipes')
    category = models.ForeignKey(RecipeCategory, null=True, on_delete=models.SET_NULL, related_name='ingredient')


    @property
    def nutrients(self):

        """
        Returns a dict of total nutrients for the recipe.
        Scales each ingredient by its quantity and unit.
        """

        total = {}

        for ri in self.recipe_ingredient.all():
            ing = ri.ingredient
            qty = ri.quantity
            unit_str = ri.unit

            try:
                unit_obj = ing.measurement_units.get(unit=unit_str)
            except IngredientMeasurementUnit.DoesNotExist:
                continue

            ing_totals = ing.get_nutrients_dict(starting_unit=unit_obj, starting_quantity=qty)

            for nutrient, value in ing_totals.items():
                total[nutrient] = total.get(nutrient, 0) + value

        return total


    @property
    def quantity_ingredients(self):
        return {ri.ingredient: (ri.quantity, ri.unit) for ri in self.recipe_ingredients.all()}




class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredient')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    quantity = models.FloatField()
    unit = models.CharField(max_length=10, choices=IngredientMeasurementUnit.MeasureUnits.choices)


    class Meta:
        unique_together = ('recipe', 'ingredient')
