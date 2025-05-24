from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend

from .models import SubscriptionsTypes, Subscriptions
from .serializers import (
    TypesSerializer,
    SubscriptionsDetailSerializer,
    SubscriptionsListSerializer,
    SubscriptionsUpdateSerializer
)
from .permissions import IsAuthor


@api_view(('GET',))
def status_list(request):
    status_choices = Subscriptions.STATUS_CHOICES
    data = [
        {'name': status[0], 'description': status[1]}
        for status in status_choices
    ]
    return Response(
        status=status.HTTP_200_OK,
        data=data
    )


class TypesListView(ListAPIView):
    queryset = SubscriptionsTypes.objects.all()
    serializer_class = TypesSerializer


class SubscriptionsViewSet(viewsets.ModelViewSet):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsDetailSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAuthor
    ]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('status',)

    def get_queryset(self):
        queryset = Subscriptions.objects.filter(
            user=self.request.user
        ).order_by('-price')
        type = self.request.GET.get('type', '')
        print(type)
        if type:
            queryset = queryset.filter(type__name=type)
        return queryset

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ('partial_update'):
            return SubscriptionsUpdateSerializer
        elif self.action in ('list'):
            return SubscriptionsListSerializer
        return super().get_serializer_class(*args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
        detail_serializer = SubscriptionsDetailSerializer(updated_instance)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)

