from rest_framework import serializers

from .models import SubscriptionsTypes, Subscriptions


class TypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionsTypes
        fields = (
            'id',
            'name',
            'slug'
        )


# class SubscriptionsSerializer(serializers.ModelSerializer):
#     end_date = serializers.SerializerMethodField()

#     class Meta:
#         model = Subscriptions
#         fields = (
#             'id',
#             'sub_name',
#             'price',
#             'type',
#             'start_date',
#             'frequency_month',
#             'status',
#             'trial_period_days',
#             'notify_before_days',
#             'is_auto_renewal'
#         )

#         extra_kwargs = {
#             'start_date': {'write_only': True},
#             'frequency_month': {'write_only': True}
#         }

#     def get_end_date(self, obj):
#         return obj.end_date

#     def create(self, validated_data):
#         validated_data['user'] = self.context['request'].user

#         return super().create(validated_data)


class SubscriptionsListSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='type.name')
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = Subscriptions
        fields = (
            'id',
            'sub_name',
            'type',
            'price',
            'end_date'
        )

    def get_end_date(self, obj):
        return obj.end_date


class SubscriptionsDetailSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.name')

    class Meta:
        model = Subscriptions
        field = {
            'id',
            'sub_name',
            'price',
            'type',
            'type_name',
            'start_date',
            'status',
            'frequency_month',
            'trial_period_days',
            'notify_before_days',
            'is_auto_renewal',
            'end_date'
        }
        read_only_field = (
            'id',
            'type_name',
            'end_date'
        )

        extra_kwargs = {
            'type': {'write_only': True},
        }

    def get_end_date(self, obj):
        return obj.end_date


class SubscriptionsUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscriptions
        fields = (
            'sub_name',
            'price',
            'start_date',
            'status',
            'notify_before_days'
        )
