import json

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
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

            print(f"errors: {form.errors}")

        # else:
        #     name_errors = form.errors.get('name', [])
        #     if any('already exists' in e for e in name_errors):
        #         name = request.POST.get('name', '').strip().lower()
        #         messages.error(request, f'"{name}" already exists.')

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
            return redirect('edit_ingredient', ingredient_id=ingredient.id)
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

# Edit
def edit_category_ajax(request, pk):
    if request.method == "POST":
        cat = IngredientCategory.objects.filter(pk=pk).first()
        if not cat: return JsonResponse({"error": "Not found"}, status=404)
        name = request.POST.get("name")
        if not name: return JsonResponse({"error": "Name required"}, status=400)
        cat.name = name
        cat.save()
        return JsonResponse({"id": cat.id, "name": cat.name})

# Delete
def delete_category_ajax(request, pk):
    if request.method == "POST":
        cat = IngredientCategory.objects.filter(pk=pk).first()
        if not cat: return JsonResponse({"error": "Not found"}, status=404)
        cat.delete()
        return JsonResponse({"success": True})


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

# Edit dietary tag
def edit_dietary_tag_ajax(request, pk):
    if request.method == "POST":
        tag = IngredientDietaryTag.objects.filter(pk=pk).first()
        if not tag:
            return JsonResponse({"error": "Not found"}, status=404)
        name = request.POST.get("name")
        if not name:
            return JsonResponse({"error": "Name required"}, status=400)
        tag.name = name
        tag.save()
        return JsonResponse({"id": tag.id, "name": tag.name})

# Delete dietary tag
def delete_dietary_tag_ajax(request, pk):
    if request.method == "POST":
        tag = IngredientDietaryTag.objects.filter(pk=pk).first()
        if not tag:
            return JsonResponse({"error": "Not found"}, status=404)
        tag.delete()
        return JsonResponse({"success": True})


def add_measurement_unit(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    if request.method == 'POST':
        unit_id = request.POST.get('unit')
        conversion = request.POST.get('conversion_to_base')

        if not conversion:
            messages.error(request, 'Conversion to base is required.')
            return redirect(reverse('edit_ingredient', kwargs={'ingredient_id': ingredient_id}) + '#additional-units')

        try:
            conversion_float = float(conversion)
        except ValueError:
            messages.error(request, 'Please enter a valid number for conversion.')
            return redirect(reverse('edit_ingredient', kwargs={'ingredient_id': ingredient_id}) + '#additional-units')

        if conversion_float <= 0:
            messages.error(request, 'Conversion to base must be greater than 0.')
            return redirect(reverse('edit_ingredient', kwargs={'ingredient_id': ingredient_id}) + '#additional-units')

        if unit_id:
            unit = get_object_or_404(MeasurementUnit, pk=unit_id)
            obj, created = IngredientMeasurementUnit.objects.get_or_create(
                ingredient=ingredient,
                unit=unit,
                defaults={'conversion_to_base': conversion_float}
            )
            if not created:
                messages.error(request, f'"{unit.name_singular}" is already added for this ingredient.')
            else:
                messages.success(request, f'"{unit.name_singular}" added successfully.')
    return redirect(reverse('edit_ingredient', kwargs={'ingredient_id': ingredient_id}) + '#additional-units')


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


def delete_measurement_unit(request, ingredient_id, imu_id):
    imu = get_object_or_404(IngredientMeasurementUnit, pk=imu_id)
    if request.method == 'POST':
        imu.delete()
    return redirect('edit_ingredient', ingredient_id=ingredient_id)

def list_categories_ajax(request):
    cats = IngredientCategory.objects.all().order_by('name')
    return JsonResponse({'items': [
        {
            'id': c.id,
            'name': c.name,
            'edit_url': reverse('edit_category_ajax', kwargs={'pk': c.id}),
            'delete_url': reverse('delete_category_ajax', kwargs={'pk': c.id}),
            'edit_fields': [
                {'key': 'name', 'placeholder': 'Name', 'value': c.name},
            ]
        }
        for c in cats
    ]})


def list_dietary_tags_ajax(request):
    tags = IngredientDietaryTag.objects.all().order_by('name')
    return JsonResponse({'items': [
        {
            'id': t.id,
            'name': t.name,
            'edit_url': reverse('edit_dietary_tag_ajax', kwargs={'pk': t.id}),
            'delete_url': reverse('delete_dietary_tag_ajax', kwargs={'pk': t.id}),
            'edit_fields': [
                {'key': 'name', 'placeholder': 'Name', 'value': t.name},
            ]
        }
        for t in tags
    ]})


def list_measurement_units_ajax(request):
    units = MeasurementUnit.objects.all().order_by('name_singular')
    return JsonResponse({'items': [
        {
            'id': u.id,
            'name': f'{u.name_singular} ({u.code})',
            'edit_url': reverse('edit_measurement_unit_ajax', kwargs={'pk': u.id}),
            'delete_url': reverse('delete_measurement_unit_ajax', kwargs={'pk': u.id}),
            'edit_fields': [
                {'key': 'name_singular', 'placeholder': 'Singular (e.g. gram)', 'value': u.name_singular},
                {'key': 'name_plural', 'placeholder': 'Plural (e.g. grams)', 'value': u.name_plural},
                {'key': 'code', 'placeholder': 'Code (e.g. g)', 'value': u.code},
            ]
        }
        for u in units
    ]})

def edit_measurement_unit_ajax(request, pk):
    if request.method == 'POST':
        unit = get_object_or_404(MeasurementUnit, pk=pk)
        name_singular = request.POST.get('name_singular', '').strip()
        name_plural = request.POST.get('name_plural', '').strip()
        if not name_singular:
            return JsonResponse({'error': 'Name is required.'}, status=400)
        unit.name_singular = name_singular
        if name_plural:
            unit.name_plural = name_plural
        unit.save()
        return JsonResponse({'id': unit.id, 'name': f'{unit.name_singular} ({unit.code})'})
    return JsonResponse({'error': 'Invalid method.'}, status=405)

def delete_measurement_unit_ajax(request, pk):
    if request.method == 'POST':
        unit = get_object_or_404(MeasurementUnit, pk=pk)
        unit.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid method.'}, status=405)


def dietary_tags_fragment(request):
    form = IngredientAddForm()
    return HttpResponse(str(form['dietary_tag']))

def edit_measurement_unit_conversion(request, ingredient_id, imu_id):
    imu = get_object_or_404(IngredientMeasurementUnit, pk=imu_id)
    if request.method == 'POST':
        conversion = request.POST.get('conversion_to_base')
        try:
            conversion_float = float(conversion)
            if conversion_float <= 0:
                messages.error(request, 'Conversion must be greater than 0.')
            else:
                imu.conversion_to_base = conversion_float
                imu.save()
                messages.success(request, 'Conversion updated.')
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid number.')
    return redirect(reverse('edit_ingredient', kwargs={'ingredient_id': ingredient_id}) + '#additional-units')