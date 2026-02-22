import json

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Ingredient, IngredientMeasurementUnit, IngredientCategory, IngredientDietaryTag, MeasurementUnit
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

                if ingredient.default_unit:
                    IngredientMeasurementUnit.objects.get_or_create(
                        ingredient=ingredient,
                        unit=ingredient.default_unit,
                        defaults={'conversion_to_base': 1}
                    )

                # Redirect to edit so user can add extra units immediately
                return redirect('edit_ingredient', ingredient_id=ingredient.id)
            except IntegrityError:
                messages.error(request, f'"{ingredient.name}" already exists.')
        else:
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

                # Ensure IngredientMeasurementUnit exists for default unit
                if ingredient.default_unit:
                    IngredientMeasurementUnit.objects.get_or_create(
                        ingredient=ingredient,
                        unit=ingredient.default_unit,
                        defaults={'conversion_to_base': 1}
                    )

            except IntegrityError:
                messages.error(request, f'"{ingredient.name}" already exists.')
                return render(request, "ingredients/edit_ingredient.html", {
                    "form": form,
                    "ingredient": ing,
                    "nutrients": Ingredient.NUTRIENTS,
                    'default_url': default_url,
                    'all_units': MeasurementUnit.objects.all().order_by('name_singular'),
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
        'all_units': MeasurementUnit.objects.all().order_by('name_singular'),
    }
    return render(request, "ingredients/edit_ingredient.html", context)


def ingredient_detail(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    default_imu = ingredient.measurement_units.filter(unit=ingredient.default_unit).first()

    selected_imu = default_imu
    quantity = ingredient.base_quantity

    if request.method == "POST":
        selected_unit_id = request.POST.get("unit")
        quantity = float(request.POST.get("quantity", ingredient.base_quantity))
        if selected_unit_id:
            selected_imu = get_object_or_404(IngredientMeasurementUnit, id=selected_unit_id)

    nutrients_dict = ingredient.get_nutrients_dict(selected_imu, quantity) if selected_imu else {}

    nutrients = {
        n: f"{round(v, 2)} {ingredient.NUTRIENT_UNITS.get(n, '')}"
        for n, v in nutrients_dict.items()
    }

    quantity = int(quantity) if quantity == int(quantity) else quantity
    unit_name = selected_imu.name_for_quantity(quantity) if selected_imu else "-"

    return render(request, "ingredients/ingredient_detail.html", {
        "ingredient": ingredient,
        "unit_name": unit_name,
        "nutrients": nutrients,
        "quantity": quantity,
        "selected_imu": selected_imu,
        "all_units": MeasurementUnit.objects.all().order_by('name_singular'),
        "no_units_defined": not selected_imu,
    })


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
        if not created:
            return JsonResponse({'error': f'"{name}" already exists.'}, status=400)
        return JsonResponse({'id': obj.id, 'name': obj.name})
    return JsonResponse({'error': 'Invalid method.'}, status=405)

def add_measurement_unit(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    if request.method == 'POST':
        unit_id = request.POST.get('unit')
        conversion = request.POST.get('conversion_to_base')
        if unit_id and conversion:
            unit = get_object_or_404(MeasurementUnit, pk=unit_id)
            IngredientMeasurementUnit.objects.get_or_create(
                ingredient=ingredient,
                unit=unit,
                defaults={'conversion_to_base': float(conversion)}
            )
    return redirect('edit_ingredient', ingredient_id=ingredient_id)

def add_measurement_unit_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code', '').strip().lower()
        name_singular = data.get('name_singular', '').strip().lower()
        name_plural = data.get('name_plural', '').strip().lower()
        if not all([code, name_singular, name_plural]):
            return JsonResponse({'error': 'All fields are required.'}, status=400)
        obj, created = MeasurementUnit.objects.get_or_create(
            code=code,
            defaults={'name_singular': name_singular, 'name_plural': name_plural}
        )
        if not created:
            return JsonResponse({'error': f'Unit with code "{code}" already exists.'}, status=400)
        return JsonResponse({'id': obj.id, 'name': f'{obj.name_singular} ({obj.code})'})
    return JsonResponse({'error': 'Invalid method.'}, status=405)


def delete_measurement_unit(request, imu_id):
    imu = get_object_or_404(IngredientMeasurementUnit, pk=imu_id)
    ingredient_id = imu.ingredient.id
    if request.method == 'POST':
        imu.delete()
    return redirect('edit_ingredient', ingredient_id=ingredient_id)