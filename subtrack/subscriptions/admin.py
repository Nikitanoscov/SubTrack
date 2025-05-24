from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import SubscriptionsTypes, Subscriptions


admin.site.register(SubscriptionsTypes)

@admin.register(Subscriptions)
class subscriptionsAdmin(admin.ModelAdmin):
    list_display = (
        'sub_name',
        'get_user_email',
        'price',
        'type',
        'status',
        'start_date',
        'frequency_month',
        'trial_period_days',
        'notify_before_days',
        'is_auto_renewal',
        'get_end_date'
    )
    search_fields = (
        'sub_name',
    )
    list_filter = ('type', 'status')

    @admin.display(description='Пользователь')
    def get_user_email(self, obj):
        link = reverse('admin:users_users_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', link, obj.user.email)

    @admin.display(description='Дата окончания')
    def get_end_date(self, obj):
        return obj.end_date
