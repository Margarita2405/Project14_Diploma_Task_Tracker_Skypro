from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserRegistrationSerializer


class RegisterView(generics.CreateAPIView):
    """Эндпоинт для регистрации нового пользователя. Доступен без аутентификации."""

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
