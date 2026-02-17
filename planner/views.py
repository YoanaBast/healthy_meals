from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from ingredients.models import Ingredient, MeasurementUnit
from planner.models import UserFridge


# Create your views here.

def manage_fridge(request):
    user = User.objects.get(username="default")
    fridge = UserFridge.objects.filter(user=user)
    ingredients = Ingredient.objects.all()


    context = {
        'fridge': fridge,
        'ingredients': ingredients,

    }
    return render(request, 'planner/manage_fridge.html', context)

def edit_fridge_item(request, item_id):
    item = get_object_or_404(UserFridge, id=item_id)

    if request.method == "POST":
        item.quantity = request.POST.get("quantity", item.quantity)
        item.unit = request.POST.get("unit", item.unit)
        item.save()
        return redirect('manage_fridge')

    context = {
        'item': item,
    }
    return render(request, 'planner/edit_fridge_item.html', context)



def add_fridge_item(request):
    if request.method == "POST":
        user, _ = User.objects.get_or_create(username="default")

        ing_id = request.POST.get("ingredient_id")
        qty = float(request.POST.get("quantity"))
        unit_id = request.POST.get("unit")

        ingredient = Ingredient.objects.get(id=ing_id)
        unit = MeasurementUnit.objects.get(id=unit_id)

        existing_item = UserFridge.objects.filter(
            user=user,
            ingredient=ingredient,
            unit=unit
        ).first()

        if existing_item:
            existing_item.quantity += qty
            existing_item.save()
        else:
            UserFridge.objects.create(
                user=user,
                ingredient=ingredient,
                quantity=qty,
                unit=unit
            )

    return redirect('manage_fridge')