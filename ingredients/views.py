from django.shortcuts import render

def manage_ingredients(request):
    return render(request, 'ingredients/manage_ingredients.html')
