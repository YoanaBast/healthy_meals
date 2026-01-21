from django.contrib import admin
from django.utils.html import mark_safe

# Register your models here.
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooking_time', 'servings', 'display_nutrients')
    search_fields = ('name',)

    def display_nutrients(self, obj):
        """
        makes nutrients show on new lines instead of in a dict

        \n doesn’t work in Django admin because admin table cells don’t render line breaks.
        Normally, Django escapes all HTML in templates and admin to prevent XSS attacks.
        Using mark_safe to force it to show it on new lines with <br>
        """
        nutrients = obj.nutrients
        return mark_safe("<br>".join(f"{k.capitalize()}: {v}" for k, v in nutrients.items()))

    display_nutrients.short_description = "Nutrients"

