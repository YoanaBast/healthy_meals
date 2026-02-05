from django.contrib import admin
from django.utils.safestring import mark_safe

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
        'default_unit',
        'base_quantity',
        'display_nutrients'
    )
    list_filter = ('category', 'dietary_tag')
    search_fields = ('name',)


    def get_dietary_tags(self, obj):
        return ", ".join([tag.name for tag in obj.dietary_tag.all()])
    get_dietary_tags.short_description = 'Dietary Tags'

    def display_nutrients(self, obj):
        nutrients = obj.nutrients
        return mark_safe("<br>".join(f"{k.capitalize()}: {v}" for k, v in nutrients.items()))
    display_nutrients.short_description = "Nutrients"
