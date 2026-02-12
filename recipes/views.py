from django.shortcuts import render, get_object_or_404, redirect

from ingredients.models import Ingredient
from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientFormSet
from .models import Recipe, RecipeCategory, RecipeIngredient


# Create your views here.

def manage_recipes(request):
    recipes = Recipe.objects.all()

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


from django.shortcuts import render, redirect
from .forms import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient


def add_recipe(request):
    recipe_form = RecipeForm()
    ingredient_formset = RecipeIngredientFormSet()
    ingredients = Ingredient.objects.prefetch_related('measurement_units__unit').all()  # <- all ingredients with units

    return render(request, 'recipes/add_recipe.html', {
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'ingredients': ingredients,  # pass to template
    })

def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect('manage_recipes')


def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/edit_recipe.html', {'form': form, 'recipe': recipe})