import djoser.views
from django.contrib.auth import get_user_model
from recipes.models import Subscribe
from recipes.serializers import SubscribeSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    CreateUserSerializer,
    TokenObtainSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(djoser.views.UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        return UserSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        subscribing = get_object_or_404(User, id=id)
        subscriber = request.user

        if request.method == 'POST':
            subscribed = (Subscribe.objects.filter(
                subscribing=subscribing, user=subscriber).exists()
            )
            if subscribed:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Subscribe.objects.get_or_create(
                user=subscriber,
                subscribing=subscribing
            )
            serializer = SubscribeSerializer(
                context=self.get_serializer_context()
            )
            return Response(serializer.to_representation(
                instance=subscribing),
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            deleted = Subscribe.objects.filter(
                user=subscriber,
                subscribing=subscribing,
            )
            Subscribe.objects.filter(
                user=subscriber,
                subscribing=subscribing,
            ).delete()
            if Subscribe.objects.filter(
                user=subscriber,
                subscribing=subscribing,
            ) == deleted:
                return Response(status=status.HTTP_304_NOT_MODIFIED)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
        url_path='subscriptions'
    )
    def subscriptions(self, request):
        current_user = request.user
        followed_list = User.objects.filter(subscribing__user=current_user)
        paginator = PageNumberPagination()
        paginator.page_size_query_param = 'limit'
        authors = paginator.paginate_queryset(
            followed_list,
            request=request
        )
        serializer = ListSerializer(
            child=SubscribeSerializer(),
            context=self.get_serializer_context()
        )
        return paginator.get_paginated_response(
            serializer.to_representation(authors)
        )


class TokenObtainView(TokenObtainPairView):
    """Получение токена."""
    serializer_class = TokenObtainSerializer
