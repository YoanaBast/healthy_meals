from django.db import models

from ingredients.models import Ingredient, IngredientMeasurementUnit


# Create your models here.

class Fridge(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=10, choices=IngredientMeasurementUnit.MeasureUnits.choices)

