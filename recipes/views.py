from django.shortcuts import render

# Create your views here.

def manage_recipes(request):
    return render(request, 'recipes/manage_recipes.html')
