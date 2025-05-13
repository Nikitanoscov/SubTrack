from django.contrib.auth import authenticate, get_user_model
from django.contrib import admin
from django.urls import include, path
from djoser.views import UserViewSet


urlpatterns = [
    path('users/register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('users/set_password/', UserViewSet.as_view({'post': 'set_password'}), name='set-password'),
    path('', include('djoser.urls.jwt')),
]