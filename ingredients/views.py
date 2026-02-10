from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Ingredient, IngredientCategory, IngredientMeasurementUnit, MeasurementUnit
from .forms import IngredientAddForm, IngredientEditForm


def manage_ingredients(request):
    ingredients = Ingredient.objects.select_related(
        'category', 'default_unit'
    ).prefetch_related(
        'dietary_tag'
    ).all().order_by('name')

    add_form = IngredientAddForm()

    context = {
        'ingredients': ingredients,
        'add_form': add_form,
        'nutrients': Ingredient.NUTRIENTS,
        'add_url': reverse('add_ingredient'),
    }

    return render(request, 'ingredients/manage_ingredients.html', context)


def add_ingredient(request):
    form = IngredientAddForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('manage_ingredients')  # reloads the page after save

    context = {
        'form': form,
        'ingredients': Ingredient.objects.select_related('category', 'default_unit')
                                         .prefetch_related('dietary_tag')
                                         .all()
                                         .order_by('name')
    }

    return render(request, 'ingredients/manage_ingredients.html', context)



def edit_ingredient(request, ingredient_id):
    default_url = reverse('manage_ingredients')
    ing = get_object_or_404(Ingredient, pk=ingredient_id)

    if request.method == "POST":
        form = IngredientEditForm(request.POST, instance=ing) #instance fills the info from the object to the form, updates instead of creating new obj
        if form.is_valid():
            form.save()  # updates, does not create new because of instance
            return redirect('manage_ingredients')  # reloads page

    else:
        form = IngredientEditForm(instance=ing)  # pre-fill with DB values

    context = {
        "form": form,
        "ingredient": ing,
        "nutrients": Ingredient.NUTRIENTS,
        'default_url': default_url,

    }

    return render(request, "ingredients/edit_ingredient.html", context)



def ingredient_detail(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    unit_id = request.GET.get("unit_id")

    if unit_id:
        selected_unit = ingredient.measurement_units.filter(id=unit_id).first()
    else:
        selected_unit = ingredient.measurement_units.first()

    # Fallback if no units exist
    if not selected_unit:
        selected_unit = None
        nutrients = ingredient.nutrients
    else:
        nutrients = ingredient.get_nutrients_dict(selected_unit, 1)  # 1 unit of selected_unit

    context = {
        "ingredient": ingredient,
        "selected_unit": selected_unit,
        'nutrients': nutrients,
    }

    return render(request, "ingredients/ingredient_detail.html", context)



def delete_ingredient(request, ingredient_id):
    ing = get_object_or_404(Ingredient, pk=ingredient_id)
    if request.method == 'POST':
        ing.delete()
        return redirect('manage_ingredients')
    return render(request, 'ingredients/ingredient_delete_confirm.html', {'ingredient': ing})