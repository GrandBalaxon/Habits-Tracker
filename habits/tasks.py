from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message, make_telegram_habit_message, get_today_send_time, \
    schedule_habit_reminder


@shared_task
def send_habit_reminder(habit_id: str) -> None:
    """
    Отправляет сообщение пользователю в Telegram чате, при наличии у оного TG ID в профиле,
    планирует задачу на следующую отправку уведомления.
    """
    try:
        habit = Habit.objects.get(id=habit_id)
    except Habit.DoesNotExist:
        return

    chat_id = habit.user.telegram_chat_id
    if not chat_id:
        return

    # Отправляем сообщение
    message = make_telegram_habit_message(habit)
    send_telegram_message(chat_id, message)

    # Высчитываем и записываем время следующего уведомления
    now = timezone.now()
    send_time = get_today_send_time(habit, now)

    next_send_time = send_time + timedelta(days=habit.periodicity)

    # Планируем новую задачу
    new_task = send_habit_reminder.apply_async(
        args=(habit.id,),
        eta=next_send_time
    )

    habit.task_id = new_task.id
    habit.next_notification = next_send_time
    habit.save(update_fields=['task_id', 'next_notification'])


@shared_task
def set_up_all_reminders() -> None:
    """Проходится по всем привычкам, создавая задачи на установку уведомлений."""
    habits = Habit.objects.filter(
        user__telegram_chat_id__isnull=False
    )
    now = timezone.now()

    for habit in habits:
        if not habit.task_id:
            schedule_habit_reminder(habit.id)
            continue
        if habit.next_notification <= now:
            schedule_habit_reminder(habit.id, revoke_old_task=True)
