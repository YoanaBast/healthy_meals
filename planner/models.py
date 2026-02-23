from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from ingredients.models import Ingredient, MeasurementUnit
from recipes.models import Recipe


# Create your models here.



class UserFridge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0, validators=[MinValueValidator(0.01)])
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('user', 'ingredient', 'unit')

    def __str__(self):
        return f"{self.user.username} - {self.ingredient.name}"


class UserGroceryList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(validators=[MinValueValidator(0.01)])
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('user', 'ingredient', 'unit')

    def __str__(self):
        return f"{self.user.username} - {self.ingredient.name}"

class GroceryListGeneration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='grocery_generations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-created_at']


class GroceryListGenerationItem(models.Model):
    generation = models.ForeignKey(GroceryListGeneration, on_delete=models.CASCADE, related_name='items')
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, blank=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null=True)
    quantity = models.FloatField(validators=[MinValueValidator(0.01)])
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.ingredient} x{self.quantity} {self.unit}"


class UserMealList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meal_list')
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)
    made_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-made_at']

    def __str__(self):
        return f"{self.user.username} — {self.recipe.name if self.recipe else 'Deleted Recipe'} — {self.made_at.strftime('%Y-%m-%d %H:%M')}"