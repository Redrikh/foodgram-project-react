import djoser.views
from django.contrib.auth import get_user_model
from recipes.models import Subscribe
from recipes.serializers import SubscribeSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    CreateUserSerializer,
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
            subscribed = Subscribe.objects.filter(
                author=subscribing,
                user=subscriber,
            ).exists()
            if subscribed or subscriber == subscribing:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Subscribe.objects.get_or_create(
                user=subscriber,
                author=subscribing
            )
            serializer = SubscribeSerializer(
                context=self.get_serializer_context()
            )
            return Response(serializer.to_representation(
                instance=subscribing),
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            deleted, _ = Subscribe.objects.filter(
                user=subscriber,
                author=subscribing,
            ).delete()
            if deleted == 0:
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
        authors = self.paginate_queryset(followed_list)
        serializer = SubscribeSerializer(
            authors,
            many=True,
            context={'request':request}
        )
        return self.get_paginated_response(serializer.data)
