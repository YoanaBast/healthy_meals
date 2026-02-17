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
    unit_name = ingredient.default_unit

    quantity = ingredient.base_quantity

    nutrients_dict  = ingredient.get_nutrients_dict(
        ingredient_unit=ingredient.default_unit,
        quantity=quantity
    )

    if request.method == "POST":
        selected_unit_id = request.POST.get("unit")
        quantity = float(request.POST.get("quantity", 0))

        if selected_unit_id and quantity:
            selected_unit = IngredientMeasurementUnit.objects.get(id=selected_unit_id)
            nutrients_dict  = ingredient.get_nutrients_dict(
                ingredient_unit=selected_unit,
                quantity=quantity
            )
            # print(f"nutrients {nutrients}") # dict!
            unit_name = selected_unit.name_for_quantity(quantity)

    nutrients = {
        n: f"{round(v, 2)} {ingredient.NUTRIENT_UNITS.get(n, '')}"
        for n, v in nutrients_dict.items()
    }
    quantity = int(quantity) if quantity == int(quantity) else quantity

    context = {
        "ingredient": ingredient,
        "unit_name": unit_name,
        'nutrients': nutrients,
        "quantity": quantity,

    }

    return render(request, "ingredients/ingredient_detail.html", context)



def delete_ingredient(request, ingredient_id):
    ing = get_object_or_404(Ingredient, pk=ingredient_id)
    if request.method == 'POST':
        ing.delete()
        return redirect('manage_ingredients')
    return render(request, 'ingredients/ingredient_delete_confirm.html', {'ingredient': ing})