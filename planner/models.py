from django.conf import settings
from django.db import models

from ingredients.models import Ingredient, IngredientMeasurementUnit, MeasurementUnit
from recipes.models import Recipe


# Create your models here.



class UserFridge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('user', 'ingredient', 'unit')

    def __str__(self):
        return f"{self.user.username} - {self.ingredient.name}"


class UserGroceryList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('user', 'ingredient', 'unit')

    def __str__(self):
        return f"{self.user.username} - {self.ingredient.name}"