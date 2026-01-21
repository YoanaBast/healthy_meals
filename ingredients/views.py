from django.shortcuts import render

def manage_ingredients(request):
    return render(request, 'ingredients/manage_ingredients.html')

def create_ingredient_more(request):
    return render(request, 'ingredients/more_ingredient_creation.html')
