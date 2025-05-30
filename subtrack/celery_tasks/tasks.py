from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from .email_template import EMAIL_TEMPLATES
from subscriptions.models import Subscriptions


Users = get_user_model()


def get_context_mail(sub_id, is_expired=None):
    try:
        sub = Subscriptions.objects.get(id=sub_id)
        context = {
            'sub_name': sub.sub_name,
            'price': sub.price,
            'end_date': sub.end_date
        }
        if is_expired:
            context['email_template'] = 'expired'
            return context
        if sub.status == 'active':
            if sub.is_auto_renewal:
                context['email_template'] = 'active_renewal'
            else:
                context['email_template'] = 'active_not_renewal'
        elif sub.status == 'trial':
            if sub.is_auto_renewal:
                context['email_template'] = 'trial_renewal'
            else:
                context['email_template'] = 'trial_not_renewal'
        return context
    except Subscriptions.DoesNotExist as err:
        print(f'Ошибка выполнения: {err}')


def should_send_notification(sub, today):
    if not sub.notify_before_days or not sub.end_date:
        return False

    notification_date = sub.end_date - timedelta(days=sub.notify_before_days)
    return today == notification_date


@shared_task
def subscriptions_notification():
    today = datetime.now().date()
    active_sub = Subscriptions.objects.filter(status='active')
    trial_sub = Subscriptions.objects.filter(status='trial')

    for sub in active_sub:
        if should_send_notification(sub, today):
            context = get_context_mail(sub.id)
            send_email_notification.delay(
                user_id=sub.user.id,
                sub_context=context,
                template_key=context['email_template'],
            )
    for sub in trial_sub:
        if should_send_notification(sub, today):
            context = get_context_mail(sub.id)
            send_email_notification.delay(
                user_id=sub.user.id,
                sub_context=context,
                template_key=context['email_template'],
            )


@shared_task
def send_email_notification(user_id, sub_context, template_key):
    try:
        user = Users.objects.get(id=user_id)
        template = EMAIL_TEMPLATES.get(template_key)
        if not template:
            raise ValueError(f"Шаблон '{template_key}' не найден")

        subject = template['subject'].format(**sub_context)
        body = template['body'].format(**sub_context)

        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )
    except Exception as err:
        print(f"[ERROR] Не удалось отправить уведомление пользователю {user_id}: {err}")
