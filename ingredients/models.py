from django.db import models

# Create your models here.

class IngredientDietaryTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class IngredientCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BaseIngredient(models.Model):
    class MeasureUnits(models.TextChoices):
        GRAM = 'g', 'Gram'
        KILOGRAM = 'kg', 'Kilogram'
        MILLILITER = 'ml', 'Milliliter'
        LITER = 'l', 'Liter'
        PIECE = 'pc', 'Piece'
        TABLESPOON = 'tbsp', 'Tablespoon'
        TEASPOON = 'tsp', 'Teaspoon'
        CUP = 'cup', 'Cup'
        OUNCE = 'oz', 'Ounce'

    name = models.CharField(max_length=100)
    min_measure_unit = models.CharField(max_length=10, choices=MeasureUnits.choices)
    base_quantity = models.FloatField(default=100, help_text="The quantity this nutrition info is based on (100 g, 1 pc, etc.)")

    category = models.ForeignKey(IngredientCategory, null=True, on_delete=models.SET_NULL, related_name='ingredient')
    # I want blank to be false to discourage users from creating lazy ingredients, this is intentional

    dietary_tag = models.ManyToManyField(IngredientDietaryTag, blank=True,  related_name='ingredient')

    base_quantity_kcal = models.FloatField(blank=True, null=True)
    base_quantity_protein = models.FloatField(blank=True, null=True)
    base_quantity_carbs = models.FloatField(blank=True, null=True)
    base_quantity_fat = models.FloatField(blank=True, null=True)
    base_quantity_fiber = models.FloatField(blank=True, null=True)
    base_quantity_sugar = models.FloatField(blank=True, null=True)
    base_quantity_salt = models.FloatField(blank=True, null=True)
    base_quantity_cholesterol = models.FloatField(blank=True, null=True)
    # Vitamins
    base_quantity_vitamin_a = models.FloatField(blank=True, null=True)
    base_quantity_vitamin_c = models.FloatField(blank=True, null=True)
    base_quantity_vitamin_d = models.FloatField(blank=True, null=True)
    base_quantity_vitamin_e = models.FloatField(blank=True, null=True)
    base_quantity_vitamin_k = models.FloatField(blank=True, null=True)
    base_quantity_vitamin_b1 = models.FloatField(blank=True, null=True)
    base_quantity_vitamin_b2 = models.FloatField(blank=True, null=True)
    base_quantity_vitamin_b3 = models.FloatField(blank=True, null=True)
    base_quantity_vitamin_b6 = models.FloatField(blank=True, null=True)
    base_quantity_vitamin_b12 = models.FloatField(blank=True, null=True)
    base_quantity_folate = models.FloatField(blank=True, null=True)
    # Minerals
    base_quantity_calcium = models.FloatField(blank=True, null=True)
    base_quantity_iron = models.FloatField(blank=True, null=True)
    base_quantity_magnesium = models.FloatField(blank=True, null=True)
    base_quantity_potassium = models.FloatField(blank=True, null=True)
    base_quantity_zinc = models.FloatField(blank=True, null=True)

    class Meta:
        abstract = True


class Ingredient(BaseIngredient):
    quantity = models.FloatField(default=1.0, help_text="Quantity in min_measure_unit")

    def __str__(self):
        return self.name

    def total_nutrient(self, nutrient_name, quantity=None):
        """
        Returns scaled nutrient value.
        - If user entered None → returns None
        - If user entered 0 → returns 0
        """
        base_value = getattr(self, f'base_quantity_{nutrient_name}')
        if base_value is None:
            return None
        qty = quantity if quantity is not None else self.quantity
        return base_value * (qty / self.base_quantity)

    @property
    def total_nutrients(self):
        """
        returns a dict of all nutrients that are filled in (more than 0)
        :return: {kcal: 123, protein:28, fat: 'Info not available', zinc: 8}
        """
        nutrients = [
            'kcal', 'protein', 'carbs', 'fat', 'fiber', 'sugar', 'salt', 'cholesterol',
            'vitamin_a', 'vitamin_c', 'vitamin_d', 'vitamin_e', 'vitamin_k',
            'vitamin_b1', 'vitamin_b2', 'vitamin_b3', 'vitamin_b6', 'vitamin_b12',
            'folate', 'calcium', 'iron', 'magnesium', 'potassium', 'zinc'
        ]
        return {
            n: (v if v is not None else 'Info not available')
            for n, v in ((n, self.total_nutrient(n)) for n in nutrients)
        }


