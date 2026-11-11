import logging

from django.db import transaction
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import Habit
from celery import current_app

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Habit)
def habit_post_save(sender, instance, created, **kwargs):
    """Планирует задачу Celery после успешного коммита в БД."""
    from .services import schedule_habit_reminder

    def schedule_task():
        if instance.notifications_on:
            try:
                schedule_habit_reminder(instance.id, force_revoke=True)
            except Exception as e:
                logger.error(f"Не удалось запланировать уведомление для привычки {instance.id}: {e}")
        elif not instance.notifications_on and instance.task_id:
            from celery import current_app
            try:
                current_app.control.revoke(instance.task_id)
                Habit.objects.filter(pk=instance.pk).update(task_id=None, next_notification=None)
            except Exception as e:
                logger.error(f"Не удалось отозвать задачу {instance.task_id}: {e}")

    # Выполняем только после успешного сохранения в БД
    transaction.on_commit(schedule_task)


@receiver(pre_delete, sender=Habit)
def habit_pre_delete(sender, instance, **kwargs):
    """Перед удалением привычки отзываем связанную задачу Celery."""
    if instance.task_id:
        try:
            current_app.control.revoke(instance.task_id)
        except Exception as e:
            logger.error(f"Не удалось отозвать задачу при удалении: {type(e).__name__}")
