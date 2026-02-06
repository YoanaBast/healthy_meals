from django.shortcuts import render, get_object_or_404, redirect
from .models import Ingredient, IngredientCategory, IngredientMeasurementUnit, MeasurementUnit


def manage_ingredients(request):
    ingredients = Ingredient.objects.all()
    categories = IngredientCategory.objects.all()
    measurement_units = MeasurementUnit.objects.all()
    context = {
        "ingredients": ingredients,
        "categories": categories,
        "measurement_units": measurement_units,
    }
    return render(request, 'ingredients/manage_ingredients.html', context)

def create_ingredient_more(request):
    return render(request, 'ingredients/more_ingredient_creation.html')

# DETAIL
def ingredient_detail(request, ingredient_id):
    ing = get_object_or_404(Ingredient, pk=ingredient_id)
    return render(request, 'ingredients/ingredient_detail.html', {'ingredient': ing})

# EDIT (minimal, no ModelForm)
def edit_ingredient(request, ingredient_id):
    ing = get_object_or_404(Ingredient, pk=ingredient_id)
    categories = IngredientCategory.objects.all()
    units = IngredientMeasurementUnit.objects.all()

    if request.method == 'POST':
        ing.name = request.POST.get('name', ing.name)
        ing.category_id = request.POST.get('category') or ing.category_id
        ing.default_unit = request.POST.get('unit', ing.default_unit)
        ing.save()
        return redirect('manage_ingredients')

    context = {
        'ingredient': ing,
        'categories': categories,
        'units': units,
    }
    return render(request, 'ingredients/ingredient_edit.html', context)

# DELETE
def delete_ingredient(request, ingredient_id):
    ing = get_object_or_404(Ingredient, pk=ingredient_id)
    if request.method == 'POST':
        ing.delete()
        return redirect('manage_ingredients')
    return render(request, 'ingredients/ingredient_delete_confirm.html', {'ingredient': ing})