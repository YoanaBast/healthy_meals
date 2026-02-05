from django.conf import settings
from django.db import models

from ingredients.models import Ingredient, IngredientMeasurementUnit


# Create your models here.

class UserFridge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username}'s Fridge"

class Fridge(models.Model):
    user_fridge = models.ForeignKey(UserFridge, on_delete=models.CASCADE, related_name='items')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=10, choices=IngredientMeasurementUnit.MeasureUnits.choices)

    def __str__(self):
        return f"{self.ingredient.name} ({self.quantity} {self.unit})"

