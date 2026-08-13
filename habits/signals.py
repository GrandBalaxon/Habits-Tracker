from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Habit
from celery import current_app


@receiver(pre_delete, sender=Habit)
def habit_pre_delete(sender, instance, **kwargs):
    """Перед удалением привычки отзываем связанную задачу Celery."""
    if instance.task_id:
        current_app.control.revoke(instance.task_id)
