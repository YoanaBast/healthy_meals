from django.contrib import admin

from planner.models import UserFridge


# Register your models here.

# planner/admin.py
from django.contrib import admin
from .models import UserFridge, UserFridge



@admin.register(UserFridge)
class UserFridgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'ingredient', 'quantity', 'unit')
    list_filter = ('user', 'unit')
    search_fields = ('user__username', 'ingredient__name')

