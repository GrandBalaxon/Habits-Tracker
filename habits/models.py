from django.core.exceptions import ValidationError
from django.db import models

from users.models import CustomUser


class Habit(models.Model):
    """
    Модель привычки. Поддерживает полезные и приятные привычки, связь между ними, периодичность выполнения и публичный доступ.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="habits")
    place = models.CharField(max_length=100, null=True, blank=True, verbose_name="Место")

    time = models.TimeField(verbose_name="Время")
    duration = models.PositiveIntegerField(verbose_name="Время на выполнение в секундах")
    periodicity = models.PositiveIntegerField(default=1, verbose_name="Периодичность в днях")

    action = models.CharField(verbose_name="Действие")
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка"
    )

    is_pleasant = models.BooleanField(verbose_name="Признак приятной привычки")
    reward = models.CharField(verbose_name="Вознаграждение", max_length=255, null=True, blank=True)
    is_public = models.BooleanField(default=False, verbose_name="Видна другим пользователям")
    task_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID задачи Celery")
    last_notification = models.DateField(null=True, blank=True, verbose_name="Время последнего оповещения")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    def clean(self):
        if self.is_pleasant and self.reward:
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения"
            )
        if self.is_pleasant and self.related_habit:
            raise ValidationError(
                "У приятной привычки не может быть связанной привычки"
            )
        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя одновременно указать вознаграждение и связанную привычку"
            )
        if self.duration > 120:
            raise ValidationError(
                "Время выполнения должно быть не больше 120 секунд"
            )
        super().clean()
