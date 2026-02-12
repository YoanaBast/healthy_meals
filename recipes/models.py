from datetime import time

from django.db import models

from ingredients.models import IngredientMeasurementUnit, Ingredient, MeasurementUnit


# Create your models here.

class RecipeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Recipe Category"
        verbose_name_plural = "Recipe Categories"


class Recipe(models.Model):
    name = models.CharField(max_length=200, unique=True)
    cooking_time = models.TimeField(null=True, blank=True)
    servings = models.PositiveIntegerField(default=1)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='recipes')
    category = models.ForeignKey(RecipeCategory, null=True, on_delete=models.SET_NULL, related_name='ingredient')
    instructions = models.TextField()

    @property
    def dietary_info(self):
        all_ingredients = self.recipe_ingredient.all()
        if not all_ingredients:
            return "-"

        # Start with the set of dietary tags from the first ingredient
        common_tags = set(all_ingredients[0].ingredient.dietary_tag.values_list('name', flat=True))

        # Intersect with the tags from all other ingredients
        for ri in all_ingredients[1:]:
            ing_tags = set(ri.ingredient.dietary_tag.values_list('name', flat=True))
            common_tags &= ing_tags

        return ", ".join(sorted(common_tags)) if common_tags else "-"

    @property
    def quantity_ingredients_list(self):
        result = []
        for ri in self.recipe_ingredient.all():
            unit = ri.unit.name_plural if ri.quantity >= 2 else ri.unit.name_singular
            quantity = int(ri.quantity) if ri.quantity == int(ri.quantity) else ri.quantity
            result.append((ri.ingredient, quantity, unit))
        return result

    @property
    def cooking_duration(self):
        """Getter: returns formatted string like '1h 30m'"""
        if not self.cooking_time:
            return "0m"
        total_minutes = self.cooking_time.hour * 60 + self.cooking_time.minute
        hours, minutes = divmod(total_minutes, 60)
        return f"{hours}h {minutes}m" if hours else f"{minutes}m"

    @cooking_duration.setter
    def cooking_duration(self, value):
        """Setter: accepts '1h 30m', '45m', or 'HH:MM:SS' like '00:10:00'
        This will be used for display purposes in admin and frontend, instead of cooking_time"""
        hours, minutes = 0, 0
        value = value.strip()
        if ":" in value:  # HH:MM[:SS] format
            parts = value.split(":")
            hours = int(parts[0])
            minutes = int(parts[1])
        else:  # '1h 30m' or '45m'
            if "h" in value:
                parts = value.split("h")
                hours = int(parts[0].strip())
                if "m" in parts[1]:
                    minutes = int(parts[1].replace("m", "").strip())
            else:
                minutes = int(value.replace("m", "").strip())
        self.cooking_time = time(hour=hours, minute=minutes)

    @property
    def kcal_per_serving(self):
        kcal = self.nutrients.get('kcal', 0)
        if self.servings and self.servings > 0:
            return round(kcal / self.servings, 2)
        return 0.0

    @property
    def nutrients_per_serving(self):
        if not self.servings or self.servings == 0:
            return {n: 0 for n in self.nutrients}
        return {n: round(v / self.servings, 2) for n, v in self.nutrients.items()}

    @property
    def nutrients_per_serving_with_units(self):
        """Nutrients per serving with units"""
        per_serving = self.nutrients_per_serving  # numeric dict
        return {n: f"{v:.2f} {Ingredient.NUTRIENT_UNITS.get(n, '')}" for n, v in per_serving.items()}

    @property
    def nutrients(self):
        total = {}
        # print(f"obj: {self.recipe_ingredient.all()}")
        for ri in self.recipe_ingredient.all():  # correct related_name
            print(f"ri: {ri}")
            ing = ri.ingredient
            qty = ri.quantity
            unit_obj = ri.unit  # already a MeasurementUnit instance

            try:
                ing_unit_obj = ing.measurement_units.get(unit=unit_obj)  # get IngredientMeasurementUnit
            except IngredientMeasurementUnit.DoesNotExist:
                continue

            ing_totals = ing.get_nutrients_dict(
                ingredient_unit=ing_unit_obj,
                quantity=qty
            )

            for nutrient, value in ing_totals.items():
                total[nutrient] = total.get(nutrient, 0) + value
        # print(f"total: {total}")
        return total

    @property
    def nutrients_with_units(self):
        """Total recipe nutrients with units"""
        total = self.nutrients  # numeric dict
        return {n: f"{v:.2f} {Ingredient.NUTRIENT_UNITS.get(n, '')}" for n, v in total.items()}


    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredient')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    quantity = models.FloatField()
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.SET_NULL, null=True)


    class Meta:
        unique_together = ('recipe', 'ingredient')
