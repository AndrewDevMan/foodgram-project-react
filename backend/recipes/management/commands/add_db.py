from csv import reader

from django.core.management.base import BaseCommand

from foodgram.settings import BASE_DIR
from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Заполнить БД ингридиентов из файла"

    def get_ingredient(self):

        if Ingredient.objects.exists():
            return self.stdout.write("База непуста.")

        self.stdout.write("Началась загрузка ингридиентов")
        with open(
                BASE_DIR / "data/ingredients.csv",
                encoding="utf8",
        ) as csvfile:
            csvreader = reader(csvfile, delimiter=",")
            data_list = [
                Ingredient(
                    name=name,
                    measurement_unit=unit,
                )
                for name, unit in csvreader
            ]
            try:
                Ingredient.objects.bulk_create(data_list)
            except ValueError as e:
                print(f"Данные {e} не валидны и добавлены не будут")
        self.stdout.write("Ингридиенты успешно добавлены.")

    def handle(self, *args, **options):
        self.get_ingredient()
