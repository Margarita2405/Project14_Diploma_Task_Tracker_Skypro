from django.conf import settings
from django.db import models


class Task(models.Model):
    """Модель задачи с полями: название, описание, статус, приоритет, ответственный пользователь,
    даты создания и обновления."""

    STATUS_CHOICES = [
        ("new", "Новая"),
        ("in_progress", "В работе"),
        ("completed", "Завершена"),
    ]
    PRIORITY_CHOICES = [
        ("low", "Низкий"),
        ("medium", "Средний"),
        ("high", "Высокий"),
    ]

    title = models.CharField(max_length=200, verbose_name="Название задачи")
    description = models.TextField(blank=True, verbose_name="Описание задачи")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус задачи")
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="medium", verbose_name="Приоритет задачи"
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks", verbose_name="Ответственный"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-created_at"]

    def __str__(self):
        """Возвращает строковое представление названия задачи."""
        return self.title
