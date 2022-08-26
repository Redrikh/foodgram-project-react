from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.mixins import IsSubscribedMixin

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя."""
    class Meta:
        fields = (
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


class TokenObtainSerializer(TokenObtainPairSerializer):
    """Сериализатор для получения токена."""
    username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs):
        current_user = get_object_or_404(
            User, username=attrs[self.username_field]
        )
        token = attrs['confirmation_code']
        if not default_token_generator.check_token(current_user, token):
            raise serializers.ValidationError(
                'Wrong confirmation code!'
            )
        refresh = RefreshToken.for_user(current_user)
        return {'token': str(refresh.access_token)}


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
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]
        model = User
