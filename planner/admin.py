from django.contrib import admin

from planner.models import Fridge


# Register your models here.

@admin.register(Fridge)
class FridgeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'quantity', 'unit')
    search_fields = ('ingredient',)


