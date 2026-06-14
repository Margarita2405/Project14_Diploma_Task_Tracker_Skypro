from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .permissions import IsAssignedUserOrReadOnly
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet для управления задачами. Поддерживает CRUD, фильтрацию, поиск и пагинацию."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAssignedUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ["status", "priority", "assigned_to"]
    ordering_fields = ["created_at", "updated_at", "priority"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        """Возвращает задачи только текущего пользователя. Суперпользователь видит все задачи."""
        user = self.request.user
        if user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)

    def perform_create(self, serializer):
        """При создании задачи автоматически назначает ответственным текущего пользователя."""
        serializer.save(assigned_to=self.request.user)
