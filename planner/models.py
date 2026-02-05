from django.conf import settings
from django.db import models

from ingredients.models import Ingredient, IngredientMeasurementUnit


# Create your models here.

class Fridge(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1  # ID of default user
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=10, choices=IngredientMeasurementUnit.MeasureUnits.choices)


