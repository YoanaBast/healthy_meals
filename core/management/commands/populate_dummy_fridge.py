from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from pathlib import Path
import json

from planner.models import UserFridge
from ingredients.models import Ingredient, MeasurementUnit


class Command(BaseCommand):
    help = "Populate user fridge from JSON"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Ensure default user exists
        default_user, created = User.objects.get_or_create(
            username="default",
            defaults={"is_superuser": True, "is_staff": True},
        )

        if created:
            default_user.set_password("defaultpassword")
            default_user.save()
            self.stdout.write(self.style.SUCCESS("Created default superuser"))

        json_path = Path(__file__).resolve().parent.parent / "dummy_data" / "dummy_fridge.json"

        if not json_path.exists():
            self.stdout.write(self.style.ERROR("File not found"))
            return

        with open(json_path, "r") as f:
            data = json.load(f)

        for item in data.get("fridge_items", []):
            name = item["name"]
            qty = item["quantity"]
            unit_code = item["unit"]

            ingredient = Ingredient.objects.filter(name=name).first()
            if not ingredient:
                self.stdout.write(self.style.WARNING(f"Skipping missing ingredient: {name}"))
                continue

            unit = MeasurementUnit.objects.filter(code=unit_code).first()
            if not unit:
                self.stdout.write(self.style.WARNING(f"Invalid unit '{unit_code}' for {name}, using default"))
                unit = ingredient.default_unit

            UserFridge.objects.update_or_create(
                user=default_user,
                ingredient=ingredient,
                defaults={
                    "quantity": qty,
                    "unit": unit,
                },
            )

            self.stdout.write(f"Added {qty} {unit} of {name}")

        self.stdout.write(self.style.SUCCESS("Fridge populated successfully"))
