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


def delete_fridge_item(request, fridge_id):
    user = User.objects.get(username="default")
    item = get_object_or_404(UserFridge, id=fridge_id, user=user)
    if request.method == "POST":
        item.delete()
    return redirect('manage_fridge')



def add_fridge_item(request):
    if request.method == "POST":
        user, _ = User.objects.get_or_create(username="default")

        ing_id = request.POST.get("ingredient_id")
        qty = float(request.POST.get("quantity"))
        unit_id = request.POST.get("unit")

        ingredient = Ingredient.objects.get(id=ing_id)
        unit = MeasurementUnit.objects.get(id=unit_id)

        # Merge-in all other fridge items of the same ingredient
        from planner.models import UserFridge
        from ingredients.models import IngredientMeasurementUnit

        explanations = []

        # Check for existing items in **any unit** of the same ingredient
        items = UserFridge.objects.filter(user=user, ingredient=ingredient)
        target_item = items.filter(unit=unit).first()

        for item in items.exclude(id=getattr(target_item, "id", None)):
            try:
                item_unit_conv = IngredientMeasurementUnit.objects.get(
                    ingredient=ingredient, unit=item.unit
                )
                target_unit_conv = IngredientMeasurementUnit.objects.get(
                    ingredient=ingredient, unit=unit
                )
            except IngredientMeasurementUnit.DoesNotExist:
                explanations.append(f"Cannot convert {item.unit} → {unit}")
                continue

            # Convert to target unit
            qty_in_base = item.quantity * item_unit_conv.conversion_to_base
            qty_in_target = qty_in_base / target_unit_conv.conversion_to_base

            if target_item:
                target_item.quantity += qty_in_target
                target_item.save()
            else:
                target_item = UserFridge.objects.create(
                    user=user,
                    ingredient=ingredient,
                    quantity=qty_in_target,
                    unit=unit
                )

            explanations.append(
                f"{item.quantity} {item.unit} → {round(qty_in_target, 2)} {unit} added"
            )

            # Delete the merged item
            item.delete()

        # Add the new quantity being submitted
        if target_item:
            target_item.quantity += qty
            target_item.save()
        else:
            target_item = UserFridge.objects.create(
                user=user,
                ingredient=ingredient,
                quantity=qty,
                unit=unit
            )

        print("----- ADD FRIDGE DEBUG -----")
        print(f"POST DATA: {request.POST}")
        print(f"USER: {user}")
        print(f"INGREDIENT OBJ: {ingredient}")
        print(f"UNIT OBJ: {unit}")
        print(f"TARGET ITEM: {target_item}")
        print("EXPLANATIONS:", explanations)
        print("----- END DEBUG -----")

    return redirect("manage_fridge")


