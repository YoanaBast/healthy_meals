from django.test import TestCase
from ingredients.models import Ingredient, IngredientCategory, IngredientMeasurementUnit
from recipes.models import Recipe, RecipeCategory, RecipeIngredient


class TestRecipeModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.recipe_cat = RecipeCategory.objects.create(name="Dinner")
        cls.ing_cat = IngredientCategory.objects.create(name="Vegetables")


        cls.carrot = Ingredient.objects.create(
            name="Carrot",
            base_quantity=100,
            category=cls.ing_cat,
            base_quantity_kcal=40,
            base_quantity_protein=1,
        )

        cls.gram_unit = IngredientMeasurementUnit.objects.create(
            ingredient=cls.carrot,
            unit=IngredientMeasurementUnit.MeasureUnits.GRAM,
            conversion_to_base=1
        )

        cls.cup_unit = IngredientMeasurementUnit.objects.create(
            ingredient=cls.carrot,
            unit=IngredientMeasurementUnit.MeasureUnits.CUP,
            conversion_to_base=120
        )

        cls.recipe = Recipe.objects.create(
            name="Carrot Salad",
            servings=2,
            category=cls.recipe_cat
        )


        cls.ri = RecipeIngredient.objects.create(
            recipe=cls.recipe,
            ingredient=cls.carrot,
            quantity=2,
            unit=IngredientMeasurementUnit.MeasureUnits.CUP
        )

    def test_recipe_str(self):
        """Test the string representation of Recipe Category"""
        self.assertEqual(str(self.recipe_cat), "Dinner")

    def test_recipe_creation(self):
        """Verify recipe is linked to ingredients correctly"""
        self.assertEqual(self.recipe.ingredients.count(), 1)
        self.assertEqual(self.recipe.ingredients.first().name, "Carrot")

    def test_recipe_nutrients_calculation(self):
        """
        Logic:
        2 cups * 120g/cup = 240g of carrots.
        Carrot has 40kcal per 100g.
        (240 / 100) * 40 = 96 kcal total.
        """

        nutrients = self.recipe.nutrients

        self.assertIn('kcal', nutrients)
        self.assertEqual(nutrients['kcal'], 96.0)
        self.assertEqual(nutrients['protein'], 2.4)

    def test_recipe_ingredient_relationship(self):
        """Check if through-model attributes are accessible"""
        recipe_ingredient = RecipeIngredient.objects.get(recipe=self.recipe)
        self.assertEqual(recipe_ingredient.quantity, 2)
        self.assertEqual(recipe_ingredient.unit, 'cup')