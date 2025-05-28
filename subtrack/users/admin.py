from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Users
from subscriptions.models import Subscriptions


@admin.register(Users)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email',
        'is_active',
    )
    list_filter = (
        'is_active',
    )
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ()}),
        ('Разрешения', {
            'fields': ('is_active', 'is_staff', 'is_superuser',)
        }),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    @admin.display(description='Количество подписок')
    def count_subscriptions(self, obj):
        return Subscriptions.objects.filter(user=obj).count()
