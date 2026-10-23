from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Убираем username из обязательных полей
    username = None

    # Делаем email уникальным и обязательным полем для авторизации
    email = models.EmailField(unique=True, verbose_name='Электронная почта')

    # Дополнительные поля по ТЗ
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар', blank=True, null=True)
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', blank=True, null=True)
    country = models.CharField(max_length=50, verbose_name='Страна', blank=True, null=True)

    # Указываем, что теперь email используется вместо логина
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
