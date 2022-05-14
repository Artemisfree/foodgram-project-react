from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Имя пользователя')
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Фамилия пользователя')
    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True,
        verbose_name='Ник',
        help_text='Ник пользователя')
    email = models.EmailField(
        db_index=True,
        unique=True,
        max_length=254,
        verbose_name='Электронная почта',
        help_text='Электронная почта пользователя')
    subscription = models.BooleanField(
        default=False,
        verbose_name='Подписка',
        help_text='Подписка на данного пользователя')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    def __str__(self):
        return self.username
