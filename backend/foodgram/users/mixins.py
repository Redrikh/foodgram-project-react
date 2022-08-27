from recipes.models import Subscribe
from rest_framework import serializers
from rest_framework.serializers import Serializer


class IsSubscribedMixin(Serializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, data):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            author=data, user=request.user
        ).exists()
