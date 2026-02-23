from django.test import TestCase

# Create your tests here.

from ingredients.models import Ingredient, IngredientCategory, IngredientDietaryTag, IngredientMeasurementUnit

class TestIngredientModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.categories = {
            "vegetables": IngredientCategory.objects.create(name="Vegetables"),
            "eggs_diary": IngredientCategory.objects.create(name="Eggs & Diary"),
        }

        cls.tags = {"vegan": IngredientDietaryTag.objects.create(name="Vegan"),
                    "sugar_free": IngredientDietaryTag.objects.create(name="Sugar Free")
                    }

    #CARROT
        cls.carrot_ingredient = Ingredient.objects.create(
            name="Carrot",
            base_quantity=100,
            category=cls.categories["vegetables"],
            base_quantity_kcal=41,
            base_quantity_protein=0.9,
        )

        cls.unit_carrot_gram = IngredientMeasurementUnit.objects.create(
            ingredient=cls.carrot_ingredient,
            unit=IngredientMeasurementUnit.MeasureUnits.GRAM,
            conversion_to_base=1,  # 1 g = 1 g
        )

        cls.unit_carrot_cup = IngredientMeasurementUnit.objects.create(
            ingredient=cls.carrot_ingredient,
            unit=IngredientMeasurementUnit.MeasureUnits.CUP,
            conversion_to_base=120, # 1 cup = 120 g
        )

        cls.carrot_ingredient.default_unit = cls.unit_carrot_gram
        cls.carrot_ingredient.save()

        cls.carrot_ingredient.dietary_tag.add(
            cls.tags["vegan"],
            cls.tags["sugar_free"]
        )

    # YOGHURT

        cls.yoghurt_ingredient = Ingredient.objects.create(
            name="Yoghurt",
            base_quantity=100,
            category=cls.categories["eggs_diary"],
            base_quantity_kcal=83,
            base_quantity_protein=1.9,
            base_quantity_calcium=0.3
        )

        cls.unit = IngredientMeasurementUnit.objects.create(
            ingredient=cls.yoghurt_ingredient,
            unit=IngredientMeasurementUnit.MeasureUnits.GRAM,
            conversion_to_base=1,  # 1 g = 1 g
        )

        cls.unit = IngredientMeasurementUnit.objects.create(
            ingredient=cls.yoghurt_ingredient,
            unit=IngredientMeasurementUnit.MeasureUnits.CUP,
            conversion_to_base=245,  # 1 cup = 245  g
        )
        cls.yoghurt_ingredient.dietary_tag.add(
            cls.tags["vegan"],
            cls.tags["sugar_free"]
        )

    # EGG

        cls.egg_ingredient = Ingredient.objects.create(
            name="Egg",
            base_quantity=1,
            category=cls.categories["eggs_diary"],
            base_quantity_kcal=199,
            base_quantity_protein=3.9,
            base_quantity_calcium=0.7
        )

        cls.egg_ingredient.dietary_tag.add(
            cls.tags["sugar_free"]
        )

        cls.unit = IngredientMeasurementUnit.objects.create(
            ingredient=cls.egg_ingredient,
            unit=IngredientMeasurementUnit.MeasureUnits.PIECE,
            conversion_to_base=1,
        )


    def test_get_nutrients_dict(self):
        cup_unit = self.carrot_ingredient.measurement_units.get(unit='cup')
        kcal = self.carrot_ingredient.get_nutrients_dict(starting_unit=cup_unit, starting_quantity=1)["kcal"]
        self.assertEqual(kcal, 49.2)

    def test_get_nutrients_dict_2(self):
        cup_unit = self.carrot_ingredient.measurement_units.get(unit='cup')
        kcal = self.carrot_ingredient.get_nutrients_dict(starting_unit=cup_unit, starting_quantity=2)["kcal"]
        self.assertEqual(kcal, 98.4)

    def get_nutrients_dict(self):
        pc_unit = self.carrot_ingredient.measurement_units.get(unit='pc')
        fat = self.egg_ingredient.get_nutrients_dict(starting_unit=pc_unit, quantity=100)["fat"]
        self.assertEqual(fat, 0)

#git check