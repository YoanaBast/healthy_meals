from django.shortcuts import render
from .models import Recipe, RecipeCategory

# Create your views here.

def manage_recipes(request):
    recipe = Recipe.objects.all()
    categories = RecipeCategory.objects.all()

    context = {
        "recipe": recipe,
        "category": categories,

    }

    return render(request, 'recipes/manage_recipes.html', context)

