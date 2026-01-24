from django.shortcuts import render
from .models import Ingredient, IngredientCategory, IngredientMeasurementUnit

def manage_ingredients(request):
    ingredients = Ingredient.objects.all()
    categories = IngredientCategory.objects.all()
    measurment_units = IngredientMeasurementUnit.objects.all()

    context = {
        "ingredients": ingredients,
        "categories": categories,
        "measurment_units": measurment_units,

    }
    return render(request, 'ingredients/manage_ingredients.html', context)

def create_ingredient_more(request):
    return render(request, 'ingredients/more_ingredient_creation.html')
