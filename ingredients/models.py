from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.


class IngredientDietaryTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ingredient Dietary Tag"
        verbose_name_plural = "Ingredient Dietary Tags"


class IngredientCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ingredient Category"
        verbose_name_plural = "Ingredient Categories"


class MeasurementUnit(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name_singular = models.CharField(max_length=50)
    name_plural = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.name_singular} ({self.code})"

class MeasurementUnitsConvert(models.Model):
    """maybe not neeeded"""
    first_unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE, related_name='first_measurment_unit')
    first_unit_quantity = models.FloatField(default=1, validators=[MinValueValidator(0.01)])

    second_unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE, related_name='second_measurment_unit')
    second_unit_quantity = models.FloatField(validators=[MinValueValidator(0.01)])



class IngredientMeasurementUnit(models.Model):
    """
    allows ingredients to have multiple measurement units - like grams and cups, conversion to base will be 1 for the main unit
    """
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, related_name='measurement_units')
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)
    conversion_to_base = models.FloatField(help_text="How much of this unit equals the base_quantity")
    # 1 cup of carrot ≈ 120 g → conversion_to_base = 120
    def name_for_quantity(self, quantity=1):
        return self.unit.name_singular if quantity == 1 else self.unit.name_plural

    @property
    def name_for_quantity_singular(self):
        return self.unit.name_singular

    @property
    def name_for_quantity_plural(self):
        return self.unit.name_plural

    def __str__(self):
        return f"{self.ingredient.name} - {self.unit}"


class Ingredient(models.Model):

    NUTRIENTS = [
        'kcal', 'protein', 'carbs', 'fat', 'fiber', 'sugar', 'salt', 'cholesterol',
        'vitamin_a', 'vitamin_c', 'vitamin_d', 'vitamin_e', 'vitamin_k',
        'vitamin_b1', 'vitamin_b2', 'vitamin_b3', 'vitamin_b6', 'vitamin_b12',
        'folate', 'calcium', 'iron', 'magnesium', 'potassium', 'zinc'
    ]
    NUTRIENT_UNITS = {
        'kcal': 'kcal',
        'protein': 'g',
        'carbs': 'g',
        'fat': 'g',
        'fiber': 'g',
        'sugar': 'g',
        'salt': 'g',
        'cholesterol': 'g',
        'vitamin_a': 'µg',
        'vitamin_c': 'mg',
        'vitamin_d': 'µg',
        'vitamin_e': 'mg',
        'vitamin_k': 'µg',
        'vitamin_b1': 'mg',
        'vitamin_b2': 'mg',
        'vitamin_b3': 'mg',
        'vitamin_b6': 'mg',
        'vitamin_b12': 'µg',
        'folate': 'µg',
        'calcium': 'mg',
        'iron': 'mg',
        'magnesium': 'mg',
        'potassium': 'mg',
        'zinc': 'mg',
    }

    name = models.CharField(max_length=100, unique=True)

    default_unit = models.ForeignKey(
        'MeasurementUnit',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )
    #the unit that holds the nutrient data for conversions

    base_quantity = models.FloatField(default=100, validators=[MinValueValidator(0.01)], help_text="The quantity the NUTRIENTS are based on in default_unit (100 g, 1 pc, etc.)")
    #base_quantity = 100 means nutrients are defined per 100g

    category = models.ForeignKey(IngredientCategory, null=True, on_delete=models.SET_NULL, related_name='ingredient')
    # discourage users from creating lazy ingredients, but if deleting a category, keep the ingredients

    dietary_tag = models.ManyToManyField(IngredientDietaryTag, blank=True,  related_name='ingredient')
    #ManyToManyField does not use null=True because the relation is stored in a separate join table

    for nutrient in NUTRIENTS:
        locals()[f'base_quantity_{nutrient}'] = models.FloatField(default=0)
    #dynamically creates a model field for each nutrient in the NUTRIENTS list

    @property
    def dietary_info(self):
        """Return dietary tags as a comma-separated string"""
        return ", ".join(tag.name for tag in self.dietary_tag.all()) or "-"

    def get_nutrients_dict(self, ingredient_unit: 'IngredientMeasurementUnit', quantity: float):
        """
        Convert nutrients to the selected ingredient measurement unit and quantity
        """
        # convert quantity to base units (e.g., grams)
        if ingredient_unit == self.default_unit:
            quantity_in_base_units = quantity
        else:
            quantity_in_base_units = quantity * ingredient_unit.conversion_to_base

        nutrients = {}
        for n in self.NUTRIENTS:
            nutrient_base_value = getattr(self, f'base_quantity_{n}', 0)
            # scale nutrient proportionally to quantity
            nutrients[n] = nutrient_base_value * (quantity_in_base_units / self.base_quantity)

        return nutrients

    @property
    def nutrients(self):
        """Return a dict of all nutrient fields with their base values -> for visualization"""
        return {n: getattr(self, f'base_quantity_{n}', 0) for n in self.NUTRIENTS}

    @property
    def nutrients_with_units(self):
        """Return nutrients with units, using NUTRIENT_UNITS dict"""
        return {n: f"{getattr(self, f'base_quantity_{n}', 0)} {self.NUTRIENT_UNITS.get(n, '')}"
                for n in self.NUTRIENTS}

    def nutrients_for_quantity(self, ingredient_unit, quantity):
        nutrients_dict = self.get_nutrients_dict(ingredient_unit, quantity)
        return {n: f"{round(v, 2)} {self.NUTRIENT_UNITS.get(n, '')}" for n, v in nutrients_dict.items()}

    def __str__(self):
        return self.name