from rest_framework import permissions


class IsAssignedUserOrReadOnly(permissions.BasePermission):
    """Разрешение: только ответственный пользователь может изменять/удалять задачу.
    Просмотр разрешён всем аутентифицированным (но через get_queryset будет фильтрация)."""

    def has_object_permission(self, request, view, obj):
        # Безопасные методы (GET, HEAD, OPTIONS) разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Остальные методы – только для ответственного
        return obj.assigned_to == request.user
