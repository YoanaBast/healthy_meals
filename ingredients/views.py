import json

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Ingredient, IngredientMeasurementUnit, IngredientCategory, IngredientDietaryTag
from .forms import IngredientAddForm, IngredientEditForm


def manage_ingredients(request):
    ingredients_qs = Ingredient.objects.select_related(
        'category', 'default_unit'
    ).prefetch_related(
        'dietary_tag'
    ).all().order_by('name')

    paginator = Paginator(ingredients_qs, 10)
    page_number = request.GET.get('page')
    ingredients = paginator.get_page(page_number)

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

    if request.method == 'POST':
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.name = ingredient.name.strip().lower()
            try:
                ingredient.save()
                form.save_m2m()
                return redirect('manage_ingredients')
            except IntegrityError:
                messages.error(request, f'"{ingredient.name}" already exists.')
        else:
            # Form invalid — check if it's specifically a duplicate name error
            name_errors = form.errors.get('name', [])
            if any('already exists' in e for e in name_errors):
                name = request.POST.get('name', '').strip().lower()
                messages.error(request, f'"{name}" already exists.')

    return render(request, 'ingredients/add_ingredient.html', {'form': form})


def edit_ingredient(request, ingredient_id):
    default_url = reverse('manage_ingredients')
    ing = get_object_or_404(Ingredient, pk=ingredient_id)

    if request.method == "POST":
        form = IngredientEditForm(request.POST, instance=ing)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.name = ingredient.name.strip().lower()
            try:
                ingredient.save()
                form.save_m2m()
            except IntegrityError:
                messages.error(request, f'"{ingredient.name}" already exists.')
                return render(request, "ingredients/edit_ingredient.html", {
                    "form": form,
                    "ingredient": ing,
                    "nutrients": Ingredient.NUTRIENTS,
                    'default_url': default_url,
                })
            return redirect('manage_ingredients')
        else:
            name_errors = form.errors.get('name', [])
            if any('already exists' in e for e in name_errors):
                name = request.POST.get('name', '').strip().lower()
                messages.error(request, f'"{name}" already exists.')
    else:
        form = IngredientEditForm(instance=ing)

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

def add_category_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name', '').strip().lower()
        if not name:
            return JsonResponse({'error': 'Name is required.'}, status=400)
        obj, created = IngredientCategory.objects.get_or_create(name=name)
        if not created:
            return JsonResponse({'error': f'"{name}" already exists.'}, status=400)
        return JsonResponse({'id': obj.id, 'name': obj.name})
    return JsonResponse({'error': 'Invalid method.'}, status=405)


def add_dietary_tag_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name', '').strip().lower()
        if not name:
            return JsonResponse({'error': 'Name is required.'}, status=400)
        obj, created = IngredientDietaryTag.objects.get_or_create(name=name)
        return JsonResponse({'id': obj.id, 'name': obj.name})  # always 200
    return JsonResponse({'error': 'Invalid method.'}, status=405)