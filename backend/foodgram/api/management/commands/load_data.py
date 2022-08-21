import csv

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient, Tag
from users.models import User


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
        with open(
            f'{data_path}/data/tags.csv',
            'r',
            encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            for tag in reader:
                name, slug, color = tag
                try:
                    Tag.objects.get_or_create(
                        name=name,
                        slug=slug,
                        color=color,
                    )
                except Exception:
                    print(f'Tag {name} '
                          f'уже есть в базе')
        self.stdout.write(self.style.SUCCESS('Все tags загружены!'))
        with open(
            f'{data_path}/data/users.csv',
            'r',
            encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            for user in reader:
                email, username, first_name, last_name, password = user
                try:
                    User.objects.get_or_create(
                        email=email,
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        password=password,
                    )
                except Exception:
                    print(f'User {username} '
                          f'уже есть в базе')
        self.stdout.write(self.style.SUCCESS('Все users загружены!'))
