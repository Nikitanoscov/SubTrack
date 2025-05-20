from django.urls import include, path
from djoser.views import UserViewSet


urlpatterns = [
    path('', include('user.urls')),
]
