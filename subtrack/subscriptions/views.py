from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import SubscriptionsTypes, Subscriptions
from .serializers import TypesSerializer


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
