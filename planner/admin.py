from django.contrib import admin

from planner.models import UserFridge


# Register your models here.

# planner/admin.py
from django.contrib import admin
from .models import UserFridge, UserGroceryList, GroceryListGeneration, GroceryListGenerationItem, UserMealList



@admin.register(UserFridge)
class UserFridgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'ingredient', 'quantity', 'unit')
    list_filter = ('user', 'unit')
    search_fields = ('user__username', 'ingredient__name')


@admin.register(UserGroceryList)
class UserGroceryListAdmin(admin.ModelAdmin):
    list_display = ('user', 'ingredient', 'quantity', 'unit')

@admin.register(GroceryListGeneration)
class GroceryListGenerationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')

@admin.register(GroceryListGenerationItem)
class GroceryListGenerationItemAdmin(admin.ModelAdmin):
    list_display = ('generation', 'recipe', 'ingredient', 'quantity', 'unit')

@admin.register(UserMealList)
class UserMealListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'made_at')