from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Ingredient, IngredientCategory, IngredientMeasurementUnit, MeasurementUnit
from .forms import IngredientForm


def manage_ingredients(request):
    ingredients = Ingredient.objects.select_related(
        'category', 'default_unit'
    ).prefetch_related(
        'dietary_tag'
    ).all().order_by('name')

    form = IngredientForm()

    context = {
        'ingredients': ingredients,
        'form': form,
        'nutrients': Ingredient.NUTRIENTS,
        'add_url': reverse('add_ingredient_popup'),  # important
    }

    return render(request, 'ingredients/manage_ingredients.html', context)


def add_ingredient_popup(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save()
            return JsonResponse({
                'success': True,
                'id': ingredient.id,
                'name': ingredient.name,
                'category': ingredient.category.name if ingredient.category else '-',
                'unit': ingredient.default_unit.name if ingredient.default_unit else '-',
            })
        return JsonResponse({'success': False, 'errors': form.errors})

def edit_ingredient_popup(request, ingredient_id):
    ing = get_object_or_404(Ingredient, pk=ingredient_id)

    if request.method == "POST":
        form = IngredientForm(request.POST, instance=ing)
        if form.is_valid():
            form.save()  # updates, does not create new
            return JsonResponse({
                "success": True,
                "id": ing.id,
                "name": ing.name,
                "category": ing.category.name if ing.category else "-",
                "unit": ing.default_unit.name if ing.default_unit else "-",
            })
        return JsonResponse({"success": False, "errors": form.errors})

    else:
        form = IngredientForm(instance=ing)  # pre-fill with DB values

    return render(request, "ingredients/edit_ingredient_modal.html", {
        "form": form,
        "ingredient": ing,
        "nutrients": Ingredient.NUTRIENTS,
    })

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