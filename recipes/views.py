from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from ingredients.models import Ingredient
from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientFormSet
from .models import Recipe, RecipeCategory, RecipeIngredient

# Create your views here.

def manage_recipes(request):
    user = User.objects.get(username="default")  # temporary default, later will use user = request.user
    recipes = Recipe.objects.all()

    for rec in recipes:
        rec.is_fav = rec.favourited_by.filter(id=user.id).exists()

    # Forms for the add modal
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
        recipe_form = RecipeForm(request.POST)
        ingredient_formset = RecipeIngredientFormSet(request.POST)

        if recipe_form.is_valid() and ingredient_formset.is_valid():
            recipe = recipe_form.save()  # save recipe first
            ingredient_formset.instance = recipe  # link formset to recipe
            ingredient_formset.save()  # save ingredients
            return redirect('manage_recipes')
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
    ingredients = Ingredient.objects.prefetch_related('measurement_units__unit').all()

    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, instance=recipe)
        ingredient_formset = RecipeIngredientFormSet(request.POST, instance=recipe)

        if recipe_form.is_valid() and ingredient_formset.is_valid():
            recipe_form.save()
            ingredient_formset.save()
            return redirect('recipe_detail', pk=recipe.pk)

    else:
        recipe_form = RecipeForm(instance=recipe)
        ingredient_formset = RecipeIngredientFormSet(instance=recipe)

    context = {
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'ingredients': ingredients,
        'recipe': recipe,
        'default_url': default_url,
    }

    return render(request, 'recipes/edit_recipe.html', context)


def toggle_favourite(request, id):
    user = get_object_or_404(User, username="default")
    recipe = get_object_or_404(Recipe, id=id)

    # toggle
    if recipe.favourited_by.filter(id=user.id).exists():
        recipe.favourited_by.remove(user)
        status = False
    else:
        recipe.favourited_by.add(user)
        status = True

    return JsonResponse({"favourited": status})