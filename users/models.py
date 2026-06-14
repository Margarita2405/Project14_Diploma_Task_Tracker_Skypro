from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Кастомный менеджер пользователей, использующий email в качестве идентификатора."""

    def create_user(self, email, password=None, **extra_fields):
        """Создаёт и сохраняет обычного пользователя."""
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создаёт суперпользователя с правами администратора."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя с авторизацией по email."""

    email = models.EmailField(unique=True, verbose_name="Электронная почта")  # Основной идентификатор
    username = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Имя пользователя"
    )  # Необязательное имя
    is_active = models.BooleanField(default=True, verbose_name="Активен")  # Активен ли пользователь
    is_staff = models.BooleanField(default=False, verbose_name="Доступ разрешен")  # Доступ в админку

    objects = UserManager()

    USERNAME_FIELD = "email"  # Поле, используемое для входа
    REQUIRED_FIELDS = []  # Обязательные поля (кроме email)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """Возвращает строковое представление пользователя."""
        return self.email
