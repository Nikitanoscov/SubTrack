from rest_framework import serializers

from .models import SubscriptionsTypes


class TypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionsTypes
        fields = (
            'id',
            'name',
            'slug'
        )
