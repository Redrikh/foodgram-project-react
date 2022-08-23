from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    email = models.EmailField('E-mail', max_length=254, unique=True)
    username = models.CharField('Username', max_length=150, unique=True)
    first_name = models.CharField('First name', max_length=150, unique=True)
    last_name = models.CharField('Last name', max_length=150, unique=True)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username
