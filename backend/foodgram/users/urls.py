from django.urls import include, path
from .views import TokenObtainView


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('', include('djoser.urls.jwt')),
    path(
        'token/',
        TokenObtainView.as_view(),
        name='token_obtain_pair'
    ),
]
