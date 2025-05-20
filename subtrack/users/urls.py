from django.urls import include, path
from djoser.views import UserViewSet


urlpatterns = [
    path(
        'register/',
        UserViewSet.as_view({'post': 'create'}),
        name='register'
    ),
    path(
        'set_password/',
        UserViewSet.as_view({'post': 'set_password'}),
        name='set-password'
    ),
    path(
        '',
        include('djoser.urls.jwt')
    ),
]