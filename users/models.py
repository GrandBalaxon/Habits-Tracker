from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('У суперпользователя должен быть задан параметр is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('У суперпользователя должен быть задан параметр is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Кастомная модель пользователя для проекта."""
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True, default=None)
    telegram_chat_id = models.CharField(
        max_length=50, null=True, blank=True, default=None, verbose_name="Telegram Chat ID"
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
