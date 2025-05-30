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


class SubscriptionsListSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='type.name')
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = Subscriptions
        fields = (
            'id',
            'sub_name',
            'type',
            'status',
            'price',
            'end_date'
        )

    def get_end_date(self, obj):
        return obj.end_date


class SubscriptionsDetailSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(
        source='type.name',
        required=False
    )

    class Meta:
        model = Subscriptions
        fields = (
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
        )
        read_only_fields = (
            'id',
            'type_name',
            'end_date'
        )

        extra_kwargs = {
            'type': {'write_only': True},
        }

    def get_end_date(self, obj):
        return obj.end_date

    def validate(self, attrs):
        data = super().validate(attrs)
        status = data.get('status', '')
        user = self.context['request'].user
        sub_name = data.get('sub_name', '')
        trial_period_days = data.get('trial_period_days', '')
        if status == 'trial' and not trial_period_days:
            raise serializers.ValidationError(
                'Для бесплатной подписки должен быть указан бесплатные период'
            )
        if Subscriptions.objects.filter(
            user=user,
            sub_name=sub_name
        ).exists():
            raise serializers.ValidationError(
                'Подписка с таким названием уже существует'
            )
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        return super().create(validated_data)


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
