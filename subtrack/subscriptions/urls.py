from django.urls import include, path

from .views import TypesListView, status_list


urlpatterns = [
    path('category/', TypesListView.as_view(), name='category-list'),
    path('status/', status_list, name='status-list')
]
