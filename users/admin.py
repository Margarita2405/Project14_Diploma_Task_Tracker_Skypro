from django.contrib import admin
from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    """Кастомная настройка панели администратора для модели User.
    Использует базовый ModelAdmin вместо UserAdmin во избежание  ошибок с отсутствующими
    полями (first_name, last_name, date_joined)."""
    list_display = ("email", "username", "is_staff", "is_active")
    search_fields = ("email", "username")
    ordering = ("email",)

    # Отображение полей при редактировании профиля
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Личные данные", {"fields": ("username",)}),
        ("Права доступа", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login",)}),
    )

    # Говорим админке использовать только существующие связи для поиска по группам
    filter_horizontal = ("groups", "user_permissions")
