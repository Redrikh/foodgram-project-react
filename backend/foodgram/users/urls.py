from django.urls import include, path

from .views import TokenObtainView

urlpatterns = [
    path('', include('djoser.urls.authtoken')),
]
