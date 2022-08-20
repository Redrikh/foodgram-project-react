import csv

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка из csv файла'

    def handle(self, *args, **kwargs):
        data_path = settings.BASE_DIR
        with open(
            f'{data_path}/data/ingredients.csv',
            'r',
            encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            for ingredient in reader:
                name, measurement = ingredient
                try:
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement=measurement
                    )
                except Exception:
                    print(f'Ингредиент {name} {measurement} '
                          f'уже есть в базе')
        self.stdout.write(self.style.SUCCESS('Все ингридиенты загружены!'))
