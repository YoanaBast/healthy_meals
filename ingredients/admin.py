from django.contrib import admin

# Register your models here.
from .models import Ingredient, IngredientCategory, IngredientDietaryTag


@admin.register(IngredientDietaryTag)
class IngredientDietaryTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(IngredientCategory)
class IngredientCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'base_quantity_kcal',
        'base_quantity_protein',
        'base_quantity_carbs',
        'base_quantity_fat',
    )
    list_filter = ('category', 'dietary_tag')
    search_fields = ('name',)


