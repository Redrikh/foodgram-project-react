from django.urls import include, path
from recipes.views import IngredientsViewSet, RecipeViewSet, TagsViewSet
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

router = DefaultRouter()

router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path(
        'users/subscriptions/',
        UserViewSet.as_view({'get': 'subscriptions', }),
        name='subscriptions',
    ),
    path('', include(router.urls)),
    path('auth/', include('users.urls')),
]
