from django.urls import include, path
from rest_framework.routers import DefaultRouter
from recipes.views import IngredientsViewSet, RecipeViewSet, TagsViewSet
from users.views import UserViewSet


router = DefaultRouter()

router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path(
        'users/subscriptions/',
        UserViewSet.as_view({'get': 'subscriptions', }),
        name='subscriptions',
    ),
    path('', include(router.urls)),
    path('auth/', include('users.urls')),
]
