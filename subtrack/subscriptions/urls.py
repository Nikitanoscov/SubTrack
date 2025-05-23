from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TypesListView, status_list, SubscriptionsViewSet


router = DefaultRouter()

router.register(
    'subscriptions',
    SubscriptionsViewSet,
    'subscription'
)


urlpatterns = [
    path('category/', TypesListView.as_view(), name='category-list'),
    path('status/', status_list, name='status-list'),
    path('', include(router.urls))
]
