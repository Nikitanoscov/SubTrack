from djoser.views import UserViewSet as DjoserViewSet
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Пользователи'])
class UserViewSet(DjoserViewSet):
    pass
