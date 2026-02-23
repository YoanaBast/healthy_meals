import json

from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from ingredients.models import Ingredient, IngredientMeasurementUnit
from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientFormSet
from .models import Recipe, RecipeCategory, RecipeIngredient

# Create your views here.

def manage_recipes(request):
    user = User.objects.get(username="default")
    recipes_qs = Recipe.objects.all().order_by('name')
    paginator = Paginator(recipes_qs, 10)
    page_number = request.GET.get('page')
    recipes = paginator.get_page(page_number)

    for rec in recipes:
        rec.is_fav = rec.favourited_by.filter(id=user.id).exists()

    recipe_form = RecipeForm()
    ingredient_form = RecipeIngredientForm()

    context = {
        'recipes': recipes,
        'recipe_form': recipe_form,
        'ingredient_form': ingredient_form,
    }
    return render(request, 'recipes/manage_recipes.html', context)


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


def add_recipe(request):
    ingredients = Ingredient.objects.prefetch_related('measurement_units__unit').all()

    if request.method == 'POST':
        print("DEBUG: POST data =", request.POST)  # <-- see all form fields
        recipe_form = RecipeForm(request.POST)
        ingredient_formset = RecipeIngredientFormSet(request.POST)

        print("DEBUG: recipe_form.is_valid() =", recipe_form.is_valid())
        print("DEBUG: recipe_form.errors =", recipe_form.errors)

        if recipe_form.is_valid() and ingredient_formset.is_valid():
            try:
                recipe = recipe_form.save(commit=False)
                print("DEBUG: recipe.category =", recipe.category)

                recipe.name = recipe.name.strip().lower()
                recipe.save()
            except IntegrityError:
                messages.error(request, f'"{recipe.name}" already exists.')
                return render(request, 'recipes/add_recipe.html', {
                    'recipe_form': recipe_form,
                    'ingredient_formset': ingredient_formset,
                    'ingredients': ingredients,
                })

            ingredient_formset.instance = recipe
            ingredient_formset.save()
            return redirect('recipe_detail', pk=recipe.pk)
        else:
            # Catch duplicate caught at form validation level
            name_errors = recipe_form.errors.get('name', [])
            if any('already exists' in e for e in name_errors):
                name = request.POST.get('name', '').strip().lower()
                messages.error(request, f'"{name}" already exists.')
    else:
        recipe_form = RecipeForm()
        ingredient_formset = RecipeIngredientFormSet()

    return render(request, 'recipes/add_recipe.html', {
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'ingredients': ingredients,
    })


def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect('manage_recipes')


def edit_recipe(request, pk):
    default_url = reverse('manage_recipes')
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, instance=recipe)
        ingredient_formset = RecipeIngredientFormSet(request.POST, instance=recipe)

        if recipe_form.is_valid() and ingredient_formset.is_valid():
            try:
                updated_recipe = recipe_form.save(commit=False)
                updated_recipe.name = updated_recipe.name.strip().lower()
                updated_recipe.save()
                ingredient_formset.save()
                return redirect('recipe_detail', pk=recipe.pk)
            except IntegrityError:
                messages.error(request, f'"{updated_recipe.name}" already exists.')
        else:
            name_errors = recipe_form.errors.get('name', [])
            if any('already exists' in e for e in name_errors):
                name = request.POST.get('name', '').strip().lower()
                messages.error(request, f'"{name}" already exists.')
    else:
        recipe_form = RecipeForm(instance=recipe)
        ingredient_formset = RecipeIngredientFormSet(instance=recipe)

    existing_ids = [form.instance.ingredient_id for form in ingredient_formset.forms if form.instance.pk]
    ingredients_add = Ingredient.objects.prefetch_related('measurement_units__unit').exclude(id__in=existing_ids)

    context = {
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'ingredients': ingredients_add,
        'recipe': recipe,
        'default_url': default_url,
    }
    return render(request, 'recipes/edit_recipe.html', context)


def toggle_favourite(request, pk):
    user = get_object_or_404(User, username="default")
    recipe = get_object_or_404(Recipe, pk=pk)

    # toggle
    if recipe.favourited_by.filter(id=user.id).exists():
        recipe.favourited_by.remove(user)
        status = False
    else:
        recipe.favourited_by.add(user)
        status = True

    return JsonResponse({"favourited": status})


def add_ingredient(request, pk):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            ingredient_id = data.get("ingredient_id")
            quantity = data.get("quantity")
            unit_id = data.get("unit_id")

            try:
                quantity = float(quantity)
                if quantity <= 0:
                    return JsonResponse({"success": False, "error": "Quantity must be greater than 0."})
            except (ValueError, TypeError):
                return JsonResponse({"success": False, "error": "Please enter a valid quantity."})

            recipe = Recipe.objects.get(pk=pk)
            ingredient = Ingredient.objects.get(pk=ingredient_id)
            unit = IngredientMeasurementUnit.objects.get(pk=unit_id)

            ri, created = RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient,
                defaults={"quantity": quantity, "unit": unit}
            )
            if not created:
                ri.quantity = quantity
                ri.unit = unit
                ri.save()

            return JsonResponse({
                "success": True,
                "ingredient_name": ingredient.name,
                "quantity": quantity,
                "unit_name": unit.name_for_quantity(quantity),
                "ingredient_id": ingredient.id,
                "unit_id": unit.id,
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})


def add_recipe_category_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name', '').strip().lower()
        if not name:
            return JsonResponse({'error': 'Name is required.'}, status=400)
        obj, created = RecipeCategory.objects.get_or_create(name=name)
        if not created:
            return JsonResponse({'error': f'"{name}" already exists.'}, status=400)
        return JsonResponse({'id': obj.id, 'name': obj.name})
    return JsonResponse({'error': 'Invalid method.'}, status=405)


def list_categories_ajax(request):
    cats = RecipeCategory.objects.all().order_by('name')
    return JsonResponse({'items': [
        {
            'id': c.id,
            'name': c.name,
            'edit_url': reverse('edit_recipe_category_ajax', kwargs={'pk': c.id}),
            'delete_url': reverse('delete_recipe_category_ajax', kwargs={'pk': c.id}),
            'edit_fields': [
                {'key': 'name', 'placeholder': 'Name', 'value': c.name},
            ]
        }
        for c in cats
    ]})


def edit_category_ajax(request, pk=None):
    print("DEBUG: edit_category_ajax called")
    print("DEBUG: URL pk =", pk)
    print("DEBUG: POST data =", request.POST)

    if request.method == "POST":
        if not pk:
            pk = request.POST.get("pk")
            print("DEBUG: fallback pk from POST =", pk)

        name = request.POST.get("name", "").strip()
        print("DEBUG: name =", name)

        if not name:
            return JsonResponse({"error": "Name required"}, status=400)

        cat = RecipeCategory.objects.filter(pk=pk).first()
        print("DEBUG: category found =", cat)

        if not cat:
            return JsonResponse({"error": "Not found"}, status=404)

        cat.name = name
        cat.save()
        print("DEBUG: category saved =", cat)

        return JsonResponse({"id": cat.id, "name": cat.name})

    return JsonResponse({"error": "Invalid method"}, status=405)



def delete_category_ajax(request, pk=None):
    print("DEBUG: delete_category_ajax called")
    print("DEBUG: URL pk =", pk)
    print("DEBUG: POST data =", request.POST)

    if request.method == "POST":
        if not pk:
            pk = request.POST.get("pk")
            print("DEBUG: fallback pk from POST =", pk)

        cat = RecipeCategory.objects.filter(pk=pk).first()
        print("DEBUG: category found =", cat)

        if not cat:
            return JsonResponse({"error": "Not found"}, status=404)

        cat.delete()
        print("DEBUG: category deleted")

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid method"}, status=405)