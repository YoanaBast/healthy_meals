from django.db import models

# Create your models here.


class IngredientDietaryTag(models.Model):

    """
    INGREDIENT DIETARY TAG
    ex: Vegan
    """

    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name




class IngredientCategory(models.Model):

    """
    INGREDIENT CATEGORY
    ex: Vegetables
    """

    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name




class IngredientMeasurementUnit(models.Model):

    """
    INGREDIENT MEASUREMENT UNIT

    allows ingredients to have multiple measurement units - like grams and cups
    """

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

    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, related_name='measurement_units')
    unit = models.CharField(max_length=10, choices=MeasureUnits.choices)
    conversion_to_base = models.FloatField(help_text="How much of this unit equals the base_quantity")


    def __str__(self):
        return f"{self.ingredient.name} - {self.unit}"




class Ingredient(models.Model):

    NUTRIENTS = [
        'kcal', 'protein', 'carbs', 'fat', 'fiber', 'sugar', 'salt', 'cholesterol',
        'vitamin_a', 'vitamin_c', 'vitamin_d', 'vitamin_e', 'vitamin_k',
        'vitamin_b1', 'vitamin_b2', 'vitamin_b3', 'vitamin_b6', 'vitamin_b12',
        'folate', 'calcium', 'iron', 'magnesium', 'potassium', 'zinc'
    ]

    name = models.CharField(max_length=100)

    default_unit = models.ForeignKey('IngredientMeasurementUnit', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    # related_name='+' tells Django not to create a reverse relation from the target model back to this one

    base_quantity = models.FloatField(default=100, help_text="The quantity the NUTRIENTS are based on in default_unit (100 g, 1 pc, etc.)")

    category = models.ForeignKey(IngredientCategory, null=True, on_delete=models.SET_NULL, related_name='ingredient')
    # discourage users from creating lazy ingredients, but if deleting a category, keep the ingredients

    dietary_tag = models.ManyToManyField(IngredientDietaryTag, blank=True,  related_name='ingredient')
    #ManyToManyField does not use null=True because the relation is stored in a separate join table

    for nutrient in NUTRIENTS:
        locals()[f'base_quantity_{nutrient}'] = models.FloatField(blank=True, null=True)
    #dynamically creates a model field for each nutrient in the NUTRIENTS list


    def scaled_nutrient(self, nutrient_name, quantity=None, unit=None):

        """
        Returns the scaled and converted value for one nutrient (like kcal, protein).
        """

        base_nutrient_value = getattr(self, f'base_quantity_{nutrient_name}', None)

        if base_nutrient_value is None or quantity is None:
            return None

        conversion = self.default_unit.conversion_to_base if self.default_unit else 1

        qty_in_base = quantity * conversion / self.base_quantity

        return round(base_nutrient_value * qty_in_base, 2)


    def total_nutrients(self, unit):

        """
        :return: {kcal: 123, protein:28, fat: 'Info not available', zinc: 8}
        """
        return {
            n: self.scaled_nutrient(n, unit=unit)
            for n in self.NUTRIENTS
        }
