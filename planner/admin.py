from django.contrib import admin

from planner.models import Fridge


# Register your models here.

# planner/admin.py
from django.contrib import admin
from .models import UserFridge, Fridge



class FridgeInline(admin.TabularInline):
    model = Fridge
    extra = 0
    readonly_fields = ('ingredient', 'quantity', 'unit')

@admin.register(UserFridge)
class UserFridgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'ingredient_list')
    inlines = [FridgeInline]

    def ingredient_list(self, obj):
        return ", ".join([f"{f.ingredient.name} ({f.quantity} {f.unit})" for f in obj.items.all()])
    ingredient_list.short_description = "Ingredients"


