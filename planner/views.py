from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from ingredients.models import Ingredient, MeasurementUnit, IngredientMeasurementUnit
from planner.forms import UserFridgeForm
from planner.models import UserFridge
from recipes.models import Recipe, RecipeIngredient


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
    user = User.objects.get(username="default")
    item = get_object_or_404(UserFridge, id=item_id, user=user)

    print("ITEM:", item)
    print("INGREDIENT:", item.ingredient)

    related_units = item.ingredient.measurement_units.all()
    print("IngredientMeasurementUnit objects:", related_units)

    units = [rel.unit for rel in related_units]
    print("UNITS:", units)

    if request.method == "POST":
        form = UserFridgeForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('manage_fridge')
    else:
        form = UserFridgeForm(instance=item)

    form.fields['unit'].queryset = MeasurementUnit.objects.filter(
        id__in=[u.id for u in units]
    )

    print("FORM UNIT QUERYSET:", form.fields['unit'].queryset)

    return render(request, 'planner/edit_fridge_item.html', {
        'form': form,
        'item': item
    })





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



def get_meal_suggestions(request):
    user = User.objects.get(username="default")
    fridge_items = UserFridge.objects.filter(user=user)
    recipes = Recipe.objects.all()

    suggestions = []

    for recipe in recipes:
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        total = recipe_ingredients.count()
        matched = 0
        missing = []

        for ri in recipe_ingredients:
            fridge_item = fridge_items.filter(ingredient=ri.ingredient).first()

            fridge_qty = 0
            if fridge_item:
                if fridge_item.unit == ri.unit.unit:
                    fridge_qty = fridge_item.quantity
                else:
                    try:
                        # convert fridge quantity to recipe unit
                        fridge_conv = IngredientMeasurementUnit.objects.get(
                            ingredient=ri.ingredient,
                            unit=fridge_item.unit
                        )
                        qty_in_base = fridge_item.quantity * fridge_conv.conversion_to_base
                        fridge_qty = qty_in_base / ri.unit.conversion_to_base
                    except IngredientMeasurementUnit.DoesNotExist:
                        fridge_qty = 0

            if fridge_qty >= ri.quantity:
                matched += 1
            else:
                missing_qty = round(max(ri.quantity - fridge_qty, 0), 2)
                unit_code = ri.unit.unit.code  # e.g., g, L
                missing.append(f"{missing_qty}{unit_code} {ri.ingredient.name}")

        match_percent = int((matched / total) * 100) if total else 0
        suggestions.append({
            "recipe": recipe,
            "match_percent": match_percent,
            "can_make": matched == total and total > 0,
            "missing_ingredients": missing
        })

    # sort best matches first
    suggestions.sort(key=lambda x: x["match_percent"], reverse=True)

    return render(request, "planner/get_meal_suggestions.html", {
        "suggestions": suggestions
    })
