from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from pathlib import Path
import json
from planner.models import Fridge
from ingredients.models import Ingredient

class Command(BaseCommand):
    help = 'Populate fridge with ingredients from JSON'

    def handle(self, *args, **kwargs):
        # Ensure default user exists
        default_user, created = User.objects.get_or_create(
            id=1,
            defaults={'username': 'default', 'is_superuser': True, 'is_staff': True}
        )
        if created:
            default_user.set_password('defaultpassword')  # set any password
            default_user.save()
            self.stdout.write(self.style.SUCCESS("Created default superuser with ID=1"))

        json_path = Path(__file__).resolve().parent.parent / 'dummy_data' / 'dummy_fridge.json'
        self.stdout.write(f"DEBUG: Looking for JSON at {json_path}")

        if not json_path.exists():
            self.stdout.write(self.style.ERROR("ERROR: File not found!"))
            return

        with open(json_path, 'r') as f:
            data = json.load(f)

        for item in data.get('fridge_items', []):
            ing_name = item['name']
            qty = item['quantity']
            unit = item['unit']

            ingredient = Ingredient.objects.filter(name=ing_name).first()
            if not ingredient:
                self.stdout.write(self.style.WARNING(f"Skipping missing ingredient: {ing_name}"))
                continue

            valid_units = [u.unit for u in ingredient.measurement_units.all()]
            if unit not in valid_units:
                self.stdout.write(self.style.WARNING(
                    f"Unit '{unit}' not valid for {ing_name}, defaulting to '{ingredient.default_unit}'"
                ))
                unit = ingredient.default_unit

            fridge_item, _ = Fridge.objects.update_or_create(
                ingredient=ingredient,
                defaults={'quantity': qty, 'unit': unit, 'user': default_user}  # assign user
            )

            self.stdout.write(f"DEBUG: Added {qty} {unit} of {ing_name} to fridge")

        self.stdout.write(self.style.SUCCESS("\nFridge populated successfully!"))
