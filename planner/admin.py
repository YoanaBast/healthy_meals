from django.contrib import admin

from planner.models import Fridge


# Register your models here.

@admin.register(Fridge)
class FridgeAdmin(admin.ModelAdmin):
    list_display = ('get_ingredients', 'quantity', 'unit')
    search_fields = ('ingredients__name',)

    # def get_ingredients(self, obj):
    #     return ", ".join([i.name for i in obj.ingredients.all()])
    # get_ingredients.short_description = 'Ingredients' --> this is the MTM version

    def get_ingredients(self, obj):
        # obj is a single Fridge instance
        return obj.ingredient.name