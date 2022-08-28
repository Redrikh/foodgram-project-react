from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers, validators

from users.mixins import IsSubscribedMixin

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя."""
    class Meta:
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        model = User

    def validate_username(self, value):
        prohibited_names = (
            'me',
            'admin',
        )
        if value in prohibited_names:
            raise serializers.ValidationError(
                f'Using name {value} is prohibited!'
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def create(self, validated_data):
        password = make_password(validated_data.pop('password'))
        return User.objects.create(password=password, **validated_data)

    def __str__(self):
        return self.username


class UserSerializer(serializers.ModelSerializer, IsSubscribedMixin):
    """Сериализатор пользователя."""
    username = serializers.CharField(
        required=True,
        validators=[validators.UniqueValidator(
            queryset=User.objects.all()
        )]
    )

    class Meta:
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]
        model = User
