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
        'activation/',
        UserViewSet.as_view({'post': 'activation'}),
        name='activation'
    ),
    path(
        '',
        include('djoser.urls.jwt')
    ),
]
