import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

DATA_PATH = os.path.join(settings.BASE_DIR, "../data")


class Command(BaseCommand):
    """Импорте данных Ингредиентов из json."""

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING("Загрузка данных из файла начата...")
        )
        with open(
            os.path.join(DATA_PATH, "ingredients.json"), encoding="utf-8"
        ) as data_file:
            data = json.loads(data_file.read())
            for item in data:
                Ingredient.objects.get_or_create(**item)
        self.stdout.write(
            self.style.SUCCESS(f"Данные из файла {data_file.name} загружены.")
        )
