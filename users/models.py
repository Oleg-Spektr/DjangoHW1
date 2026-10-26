from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# Кастомный менеджер для корректной работы команд создания пользователей по Email
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email является обязательным полем')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    # Убираем username из обязательных полей
    username = None

    # Делаем email уникальным и основным полем для авторизации
    email = models.EmailField(unique=True, verbose_name='Электронная почта')

    # Дополнительные поля по ТЗ
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар', blank=True, null=True)
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', blank=True, null=True)
    country = models.CharField(max_length=50, verbose_name='Страна', blank=True, null=True)

    # Указываем, что теперь email используется вместо логина
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Привязываем наш кастомный менеджер, чтобы запустить команды без ошибок (Критерий)
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
