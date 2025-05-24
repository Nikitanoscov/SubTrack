from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import Cast
from django.utils import timezone
from dateutil.relativedelta import relativedelta


Users = get_user_model()


class SubscriptionsManager(models.Manager):

    def with_end_date(self):
        return self.annotate(
            end_date=models.Case(
                models.When(frequency_month='0', then=models.Value(None)),
                default=Cast(
                    models.F('start_date') + relativedelta(
                        models.F('frequency_month')
                    ),
                    output_field=models.DateField()
                ),
                output_field=models.DateField()
            )
        )


class SubscriptionsTypes(models.Model):

    name = models.CharField(verbose_name='Имя', max_length=32, unique=True)
    slug = models.CharField(verbose_name='Слаг', max_length=32, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.name


class Subscriptions(models.Model):

    # возможные поля для периодичности
    FREQUENCY_CHOICES = (
        ('1', '1 Месяц'),
        ('3', '3 Месяца'),
        ('6', '6 Месяцев'),
        ('12', '12 Месяцев'),
        ('0', 'Бессрочная')
    )
    # возможные поля для статуса
    STATUS_CHOICES = (
        ('trial', 'Пробный период'),
        ('active', 'Активна'),
        ('cancelled', 'Отменена'),
    )

    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    sub_name = models.CharField(
        verbose_name='Имя подписки',
        max_length=100
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(1_000_000)]
    )
    type = models.ForeignKey(
        SubscriptionsTypes,
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )
    start_date = models.DateField(
        verbose_name='Дата начала подписки'
    )
    frequency_month = models.CharField(
        verbose_name='Переодичность подписки',
        choices=FREQUENCY_CHOICES
    )
    status = models.CharField(
        verbose_name='Статус',
        choices=STATUS_CHOICES,
        default='active'
    )
    trial_period_days = models.PositiveSmallIntegerField(
        verbose_name='Пробный период подписки',
        default=0
    )
    notify_before_days = models.SmallIntegerField(
        verbose_name='Количество дней до уведомления',
        validators=(MinValueValidator(-1), MaxValueValidator(5)),
        default=3
    )
    is_auto_renewal = models.BooleanField(
        verbose_name='Авто продление',
        default=False
    )

    objects = SubscriptionsManager()

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = [['user', 'sub_name']]

    @property
    def is_active(self):
        pass

    @property
    def is_trial(self):
        pass

    @property
    def end_date(self):
        try:
            if self.status == 'active':
                if self.frequency_month == '0':
                    return None
                month = int(self.frequency_month)

                now = datetime.now().date()
                current = self.start_date + relativedelta(months=month)
                while current <= now:
                    print(current)
                    current = current + relativedelta(months=month)
                return current
            elif self.status == 'trial':
                days_passed = relativedelta(
                    datetime.now(), self.start_date
                ).days
                start_date = self.start_date + relativedelta(days=days_passed)
                days = int(self.trial_period_days)
                result = self.start_date + relativedelta(days=days)
            else:
                return None
            return result
        except (ValueError, TypeError) as err:
            print(err)
            return None
