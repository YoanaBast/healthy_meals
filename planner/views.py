from django.core.paginator import Paginator
from django.db.models import Prefetch
from planner.forms import UserFridgeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from ingredients.models import Ingredient, MeasurementUnit, IngredientMeasurementUnit
from planner.models import UserFridge, UserGroceryList, GroceryListGeneration, GroceryListGenerationItem
from recipes.models import Recipe, RecipeIngredient

# Create your views here.

def manage_fridge(request):
    user = User.objects.get(username="default")
    fridge_list = UserFridge.objects.filter(user=user).select_related('ingredient__category', 'unit')
    ingredients = Ingredient.objects.all()

    paginator = Paginator(fridge_list, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'fridge': page_obj,  # pass page_obj instead of full queryset
        'ingredients': ingredients,
        'page_obj': page_obj,  # for pagination controls
    }

    return render(request, 'planner/manage_fridge.html', context)


def edit_fridge_item(request, item_id):
    item = get_object_or_404(UserFridge, pk=item_id)

    if request.method == 'POST':
        form = UserFridgeForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('manage_fridge')
    else:
        form = UserFridgeForm(instance=item)

    ingredient_units = item.ingredient.measurement_units.select_related('unit').all()

    return render(request, 'planner/edit_fridge.html', {
        'form': form,
        'item': item,
        'ingredient_units': ingredient_units,
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

        # print("----- ADD FRIDGE DEBUG -----")
        # print(f"POST DATA: {request.POST}")
        # print(f"USER: {user}")
        # print(f"INGREDIENT OBJ: {ingredient}")
        # print(f"UNIT OBJ: {unit}")
        # print(f"TARGET ITEM: {target_item}")
        # print("EXPLANATIONS:", explanations)
        # print("----- END DEBUG -----")

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
                        conv_fridge = IngredientMeasurementUnit.objects.get(
                            ingredient=ri.ingredient, unit=fridge_item.unit
                        )
                        qty_in_base = fridge_item.quantity * conv_fridge.conversion_to_base
                        fridge_qty = qty_in_base / ri.unit.conversion_to_base
                    except IngredientMeasurementUnit.DoesNotExist:
                        fridge_qty = 0

            if fridge_qty >= ri.quantity:
                matched += 1
            else:
                missing_qty = round(max(ri.quantity - fridge_qty, 0), 2)
                missing.append(f"{missing_qty:g}{ri.unit.unit.code} {ri.ingredient.name}")

        match_percent = int((matched / total) * 100) if total else 0
        suggestions.append({
            "recipe": recipe,
            "match_percent": match_percent,
            "can_make": matched == total and total > 0,
            "missing_ingredients": missing
        })

    suggestions.sort(key=lambda x: x["match_percent"], reverse=True)

    # Pagination
    paginator = Paginator(suggestions, 10)  # 10 suggestions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "planner/get_meal_suggestions.html", {
        "suggestions": page_obj,  # page_obj for template
        "page_obj": page_obj,
    })


def make_recipe(request, id):
    if request.method != 'POST':
        return redirect('meal_suggestions')

    recipe = get_object_or_404(Recipe, id=id)
    user = User.objects.get(username="default")
    fridge_items = UserFridge.objects.filter(user=user)

    print("---- MAKE RECIPE DEBUG ----")
    print(f"Recipe: {recipe.name}")
    print("User fridge before:", [(f.ingredient.name, f.quantity, f.unit) for f in fridge_items])

    # First, check if user has enough ingredients
    for ri in recipe.recipe_ingredient.all():
        fridge_item = fridge_items.filter(ingredient=ri.ingredient).first()
        required_qty = ri.quantity  # in ri.unit

        available_qty = 0
        if fridge_item:
            try:
                fridge_unit_obj = IngredientMeasurementUnit.objects.get(
                    ingredient=ri.ingredient,
                    unit=fridge_item.unit
                )
                # convert fridge quantity → recipe unit
                available_qty = (fridge_item.quantity * fridge_unit_obj.conversion_to_base) / ri.unit.conversion_to_base
            except IngredientMeasurementUnit.DoesNotExist:
                available_qty = 0

        print(f"Processing {ri.ingredient.name}: need {required_qty}{ri.unit.unit.code}, have {available_qty:.2f}{ri.unit.unit.code}")

        if available_qty < required_qty:
            messages.error(request, f"Not enough ingredients: {user.username} - {ri.ingredient.name}")
            return redirect('meal_suggestions')

    # Subtract ingredients from fridge
    for ri in recipe.recipe_ingredient.all():
        fridge_item = fridge_items.get(ingredient=ri.ingredient)
        fridge_unit_obj = IngredientMeasurementUnit.objects.get(
            ingredient=ri.ingredient,
            unit=fridge_item.unit
        )

        # convert recipe quantity → fridge unit
        qty_to_subtract = (ri.quantity * ri.unit.conversion_to_base) / fridge_unit_obj.conversion_to_base
        fridge_item.quantity -= qty_to_subtract

        if fridge_item.quantity <= 0:
            fridge_item.delete()
        else:
            fridge_item.save()

    messages.success(request, f"{recipe.name} was made successfully!")

    fridge_after = [(f.ingredient.name, f.quantity, f.unit) for f in UserFridge.objects.filter(user=user)]
    print("User fridge after:", fridge_after)
    print("---- END MAKE RECIPE DEBUG ----")

    return redirect('meal_suggestions')


def convert_qty_to_unit(qty, from_unit, to_unit, ingredient):
    """
    Convert qty of ingredient FROM from_unit TO to_unit using IngredientMeasurementUnit.
    Returns converted quantity or None if conversion not possible.
    """
    if from_unit == to_unit:
        return qty
    try:
        from_conv = IngredientMeasurementUnit.objects.get(ingredient=ingredient, unit=from_unit)
        to_conv = IngredientMeasurementUnit.objects.get(ingredient=ingredient, unit=to_unit)
        qty_in_base = qty * from_conv.conversion_to_base
        qty_in_target = qty_in_base / to_conv.conversion_to_base
        return qty_in_target
    except IngredientMeasurementUnit.DoesNotExist:
        return None


def generate_grocery_list(request):
    user = User.objects.get(username="default")

    from django.db.models import Exists, OuterRef
    recipes = Recipe.objects.annotate(
        is_fav=Exists(
            Recipe.favourited_by.through.objects.filter(
                recipe_id=OuterRef('pk'),
                user_id=user.id
            )
        )
    ).prefetch_related(
        Prefetch('recipe_ingredient', queryset=RecipeIngredient.objects.select_related('unit', 'ingredient'))
    ).all()

    paginator = Paginator(recipes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    selected_recipes = request.POST.getlist('recipes') or request.GET.getlist('recipes')
    selected_recipes = list(dict.fromkeys(selected_recipes))

    if request.method == "POST":
        recipe_ids = request.POST.getlist('recipes')
        recipe_ids = list(dict.fromkeys(recipe_ids))
        selected_recipes = recipe_ids

        if not recipe_ids:
            messages.warning(request, "No recipes selected!")
            return render(request, 'planner/generate_grocery_list.html', {
                'page_obj': page_obj,
                'recipes': page_obj.object_list,
                'selected_recipes': selected_recipes,
            })

        selected_recipes_qs = Recipe.objects.filter(id__in=recipe_ids).prefetch_related(
            'recipe_ingredient__ingredient',
            'recipe_ingredient__unit'
        )

        # Build needed dict keyed by ingredient id, tracking which recipe each line came from
        # needed[ing_id] = { ingredient, unit, recipes: { recipe: qty_in_base } }
        needed = {}

        for rec in selected_recipes_qs:
            for ri in rec.recipe_ingredient.all():
                ing = ri.ingredient
                base_unit = ing.default_unit

                if ing.id not in needed:
                    needed[ing.id] = {
                        'ingredient': ing,
                        'unit': base_unit,
                        'total_qty': 0,
                        'by_recipe': {},  # recipe obj -> qty in base unit
                    }

                try:
                    converted_qty = convert_qty_to_unit(ri.quantity, ri.unit.unit, base_unit, ing)
                    if converted_qty is None:
                        messages.warning(request, f"Cannot convert {ri.unit.unit.code} for {ing.name}")
                        converted_qty = ri.quantity
                except Exception:
                    messages.warning(request, f"Cannot convert unit for {ing.name}")
                    converted_qty = ri.quantity

                needed[ing.id]['total_qty'] += converted_qty
                needed[ing.id]['by_recipe'][rec] = needed[ing.id]['by_recipe'].get(rec, 0) + converted_qty

        # Subtract what's already in the fridge, only add shortfall
        fridge_items = UserFridge.objects.filter(user=user).select_related('ingredient', 'unit')

        final_needed = {}
        for ing_id, data in needed.items():
            ing = data['ingredient']
            needed_qty = data['total_qty']
            base_unit = data['unit']  # this is a MeasurementUnit object

            fridge_item = fridge_items.filter(ingredient=ing).first()
            available_in_base = 0

            if fridge_item:
                # Convert fridge quantity to base units using convert_qty_to_unit
                # which handles the same-unit case and uses IngredientMeasurementUnit lookups
                converted = convert_qty_to_unit(
                    fridge_item.quantity,
                    fridge_item.unit,   # MeasurementUnit
                    base_unit,          # MeasurementUnit
                    ing
                )
                if converted is not None:
                    available_in_base = converted
                else:
                    # Units are incompatible — warn but don't crash
                    messages.warning(
                        request,
                        f"Could not convert fridge units for {ing.name} "
                        f"({fridge_item.unit} → {base_unit}), ignoring fridge stock."
                    )

            shortfall = needed_qty - available_in_base
            if shortfall > 0:
                final_needed[ing_id] = {
                    'ingredient': ing,
                    'quantity': round(shortfall, 4),
                    'unit': base_unit,
                    'by_recipe': data['by_recipe'],
                }

        if not final_needed:
            messages.info(request, "You already have all the ingredients in your fridge!")
            return redirect('generate_grocery_list')

        # ADD to existing grocery list quantities instead of overwriting
        for ing_data in final_needed.values():
            existing = UserGroceryList.objects.filter(
                user=user,
                ingredient=ing_data['ingredient'],
                unit=ing_data['unit']
            ).first()

            if existing:
                existing.quantity += ing_data['quantity']
                existing.save()
            else:
                UserGroceryList.objects.create(
                    user=user,
                    ingredient=ing_data['ingredient'],
                    quantity=ing_data['quantity'],
                    unit=ing_data['unit']
                )

        # Record a history entry for this generation
        generation = GroceryListGeneration.objects.create(user=user)
        for ing_data in final_needed.values():
            for recipe_obj, qty in ing_data['by_recipe'].items():
                GroceryListGenerationItem.objects.create(
                    generation=generation,
                    recipe=recipe_obj,
                    ingredient=ing_data['ingredient'],
                    quantity=round(qty, 4),
                    unit=ing_data['unit'],
                )

        messages.success(request, "Ingredients added to your grocery list!")
        return redirect('user_grocery_list')

    return render(request, 'planner/generate_grocery_list.html', {
        'page_obj': page_obj,
        'recipes': page_obj.object_list,
        'selected_recipes': selected_recipes,
    })


def user_grocery_list(request):
    from collections import OrderedDict
    user = User.objects.get(username="default")
    items = UserGroceryList.objects.filter(user=user).select_related('ingredient', 'unit')

    raw_history = GroceryListGeneration.objects.filter(user=user).prefetch_related(
        'items__ingredient',
        'items__unit',
        'items__recipe',
    )

    # Group items by recipe in Python so the template stays simple
    history_data = []
    for gen in raw_history:
        by_recipe = OrderedDict()
        for item in gen.items.all():
            recipe_name = item.recipe.name if item.recipe else "Unknown Recipe"
            if recipe_name not in by_recipe:
                by_recipe[recipe_name] = []
            by_recipe[recipe_name].append(item)
        history_data.append({
            'created_at': gen.created_at,
            'by_recipe': by_recipe,
        })

    history_paginator = Paginator(history_data, 5)
    history_page_number = request.GET.get('history_page')
    history_page_obj = history_paginator.get_page(history_page_number)

    context = {
        'items': items,
        'history': history_page_obj,
        'history_page_obj': history_page_obj,
    }
    return render(request, 'planner/user_grocery_list.html', context)


def delete_grocery_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(UserGroceryList, id=item_id)
        item.delete()
    return redirect("user_grocery_list")


def add_grocery_to_fridge(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(UserGroceryList, id=item_id)

        UserFridge.objects.update_or_create(
            user=item.user,
            ingredient=item.ingredient,
            defaults={
                "quantity": item.quantity,
                "unit": item.unit,
            }
        )
        item.delete()

    return redirect("user_grocery_list")


def add_all_grocery_to_fridge(request):
    if request.method == "POST":
        user = User.objects.get(username="default")
        items = UserGroceryList.objects.filter(user=user)

        for item in items:
            UserFridge.objects.update_or_create(
                user=item.user,
                ingredient=item.ingredient,
                defaults={
                    "quantity": item.quantity,
                    "unit": item.unit,
                }
            )
        items.delete()

    return redirect("user_grocery_list")