from csv import reader

from django.core.management.base import BaseCommand

from foodgram.settings import BASE_DIR
from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Заполнить БД ингридиентов из файла"

    def get_ingredient(self):
        if Ingredient.objects.exists():
            self.stdout.write("База непуста.")
            return
        self.stdout.write("Началась загрузка ингридиентов")
        with open(
                BASE_DIR / "data/ingredients.csv",
                encoding="utf8",
        ) as csvfile:
            csvreader = reader(csvfile, delimiter=",")
            for row in csvreader:
                try:
                    Ingredient.objects.create(
                        name=row[0],
                        measurement_unit=row[1],
                    )
                except ValueError:
                    print(f"Данные {row[0]}, {row[1]} ",
                          "не валидны и добавлены не будут")
                    continue
        self.stdout.write("Ингридиенты успешно добавлены.")

    def handle(self, *args, **options):
        self.get_ingredient()
