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


    class Meta:
        verbose_name = "Ingredient Dietary Tag"
        verbose_name_plural = "Ingredient Dietary Tags"


class IngredientCategory(models.Model):

    """
    INGREDIENT CATEGORY
    ex: Vegetables
    """

    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ingredient Category"
        verbose_name_plural = "Ingredient Categories"


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
    # 1 cup of carrot ≈ 120 g → conversion_to_base = 120

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

    default_unit = models.CharField(max_length=10, choices=IngredientMeasurementUnit.MeasureUnits.choices, default=IngredientMeasurementUnit.MeasureUnits.GRAM)
    #the unit that holds the nutrient data for conversions

    base_quantity = models.FloatField(default=100, help_text="The quantity the NUTRIENTS are based on in default_unit (100 g, 1 pc, etc.)")
    #base_quantity = 100 means nutrients are defined per 100g

    category = models.ForeignKey(IngredientCategory, null=True, on_delete=models.SET_NULL, related_name='ingredient')
    # discourage users from creating lazy ingredients, but if deleting a category, keep the ingredients

    dietary_tag = models.ManyToManyField(IngredientDietaryTag, blank=True,  related_name='ingredient')
    #ManyToManyField does not use null=True because the relation is stored in a separate join table

    for nutrient in NUTRIENTS:
        locals()[f'base_quantity_{nutrient}'] = models.FloatField(default=0)
    #dynamically creates a model field for each nutrient in the NUTRIENTS list

    def get_nutrients_dict(self, starting_unit, starting_quantity):
        """
        it’s used for scaling nutrients based on a specific starting_unit and starting_quantity -> calculations
        """
        nutrients = {}

        if starting_unit.unit != self.default_unit:
            quantity_in_base_units = starting_quantity * starting_unit.conversion_to_base
        else:
            quantity_in_base_units = starting_quantity

        for n in self.NUTRIENTS:
            nutrient_name = f'base_quantity_{n}'
            nutrient_base_value = getattr(self, nutrient_name, 0) or 0

            nutrients[n] = (nutrient_base_value / self.base_quantity) * quantity_in_base_units

        # Print debug info for this ingredient
        print(f"{self.name} | {starting_quantity} {starting_unit.unit} → {quantity_in_base_units} {self.default_unit}")
        print(", ".join([f"{n}: {v:.2f}" for n, v in nutrients.items() if v > 0]))

        return nutrients

    @property
    def nutrients(self):
        """Return a dict of all nutrient fields with their base values -> for visualization"""
        return {n: getattr(self, f'base_quantity_{n}', 0) for n in self.NUTRIENTS}

    def __str__(self):
        return self.name