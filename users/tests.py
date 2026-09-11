from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserAuthTests(APITestCase):
    """Тесты регистрации и аутентификации пользователей."""

    def test_registration_success(self):
        """Проверка успешной регистрации. Ожидаемый статус: 201 Created, пользователь создан в БД."""
        url = reverse("users:auth_register")
        data = {"email": "test@example.com", "password": "qwerty123"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, "test@example.com")

    def test_registration_missing_email(self):
        """Попытка регистрации без email – ожидается ошибка валидации (400)."""
        url = reverse("users:auth_register")
        data = {"password": "qwerty123"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_obtain_success(self):
        """Получение JWT-токена для зарегистрированного пользователя.
        Ожидается успешный ответ (200) с полями access и refresh."""
        User.objects.create_user(email="test@example.com", password="qwerty123")
        url = reverse("token_obtain_pair")
        data = {"email": "test@example.com", "password": "qwerty123"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
