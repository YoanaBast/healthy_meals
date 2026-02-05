from django.contrib import admin
from django.utils.html import mark_safe

# Register your models here.
from .models import Recipe, RecipeIngredient, RecipeCategory



@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooking_duration', 'servings', 'display_ingredients', 'display_nutrients')
    search_fields = ('name',)

    def display_ingredients(self, obj):
        return ", ".join([ri.ingredient.name for ri in obj.recipe_ingredient.all()])
    display_ingredients.short_description = "Ingredients"

    def display_nutrients(self, obj):
        nutrients = obj.nutrients
        return mark_safe("<br>".join(f"{k.capitalize()}: {v}" for k, v in nutrients.items()))
    display_nutrients.short_description = "Nutrients"


@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']