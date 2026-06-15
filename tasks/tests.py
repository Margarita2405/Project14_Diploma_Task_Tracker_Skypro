from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from .models import Task


class TaskAPITests(APITestCase):
    """Тесты API для управления задачами."""

    def setUp(self):
        """Предварительная настройка: создаём тестового пользователя и авторизуем клиент."""
        self.user = User.objects.create_user(email="user@test.com", password="pass")
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        """Проверка успешного создания задачи. Ожидаемый результат: HTTP 201, объект задачи создан, ответственный
        совпадает с текущим пользователем."""
        url = reverse("task-list")
        data = {"title": "Новая задача", "description": "Описание", "priority": "high"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().assigned_to, self.user)

    def test_list_tasks_only_own(self):
        """Проверка фильтрации списка задач – пользователь должен видеть только свои задачи.
        Создаём задачу для другого пользователя и одну для текущего.
        Ожидается, что в списке будет только одна задача (своя)."""
        other_user = User.objects.create_user(email="other@test.com", password="pass")
        Task.objects.create(title="Чужая задача", assigned_to=other_user)
        Task.objects.create(title="Моя задача", assigned_to=self.user)

        url = reverse("task-list")
        response = self.client.get(url)

        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Моя задача")

    def test_update_other_user_task_forbidden(self):
        """Проверка прав доступа: попытка обновить задачу, созданную другим пользователем.
        Ожидаемый результат: HTTP 404 (задача не найдена, т.к. не принадлежит текущему пользователю)."""
        other_user = User.objects.create_user(email="other@test.com", password="pass")
        task = Task.objects.create(title="Чужая задача", assigned_to=other_user)

        url = reverse("task-detail", args=[task.id])
        data = {"title": "Попытка изменения", "status": "completed"}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_tasks_by_status(self):
        """Проверка фильтрации задач по полю 'status'.
        Создаём задачи с разными статусами и фильтруем по статусу 'new'.
        Ожидается, что в ответе будет только задача с заголовком 'Новая'."""
        Task.objects.create(title="Новая", status="new", assigned_to=self.user)
        Task.objects.create(title="В работе", status="in_progress", assigned_to=self.user)

        url = reverse("task-list") + "?status=new"
        response = self.client.get(url)

        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Новая")

    def test_pagination(self):
        """Проверка пагинации: при создании 12 задач на странице должно быть 10."""
        for i in range(12):
            Task.objects.create(title=f"Задача {i}", assigned_to=self.user)

        url = reverse("task-list")
        response = self.client.get(url)

        # Первая страница должна содержать 10 записей (PAGE_SIZE=10)
        self.assertEqual(len(response.data["results"]), 10)
        # Должна быть ссылка на следующую страницу
        self.assertIsNotNone(response.data["next"])
