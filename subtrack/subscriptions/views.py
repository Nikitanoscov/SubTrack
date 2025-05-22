from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view

from .models import SubscriptionsTypes, Subscriptions
from .serializers import (
    TypesSerializer,
    SubscriptionsDetailSerializer,
    SubscriptionsListSerializer,
    SubscriptionsUpdateSerializer
)


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

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ('partial_update'):
            return SubscriptionsUpdateSerializer
        elif self.action in ('list'):
            return SubscriptionsListSerializer
        return super().get_serializer(*args, **kwargs)

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

