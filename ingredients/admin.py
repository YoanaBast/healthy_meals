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
        'get_dietary_tags',
        'base_quantity_kcal',
        'base_quantity_protein',
        'base_quantity_carbs',
        'base_quantity_fat',
    )
    list_filter = ('category', 'dietary_tag')
    search_fields = ('name',)


    def get_dietary_tags(self, obj):
        return ", ".join([tag.name for tag in obj.dietary_tag.all()])
    get_dietary_tags.short_description = 'Dietary Tags'