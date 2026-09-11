from rest_framework import serializers

from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации новых пользователей. Пароль записывается, но не выводится."""

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "password", "username")

    def create(self, validated_data):
        """Создаёт нового пользователя с хэшированным паролем."""
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            username=validated_data.get("username", ""),
        )
        return user
