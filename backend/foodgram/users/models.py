from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_USER, 'пользователь'),
        (ROLE_ADMIN, 'администратор'),
    ]

    email = models.EmailField('E-mail', max_length=254, unique=True)
    username = models.CharField('Username', max_length=150, unique=True)
    first_name = models.CharField('First name', max_length=150, unique=True)
    last_name = models.CharField('Last name', max_length=150, unique=True)
    role = models.CharField(
        'Тип пользователя',
        max_length=30,
        choices=ROLE_CHOICES,
        default=ROLE_USER,
    )

    class Meta:
        ordering = ['username']

    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return self.username
