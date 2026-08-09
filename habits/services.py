from datetime import datetime, timedelta

import requests
from celery import current_app
from django.utils import timezone

from config import settings
from habits.models import Habit


def make_telegram_habit_message(habit: "Habit") -> str:
    """Генерирует красивое сообщение на основе заданной привычки."""
    next_time = {
        1: "24 часа",
        2: "2 дня",
        3: "3 дня",
        4: "4 дня",
        5: "5 дней",
        6: "6 дней",
        7: "неделю"
    }

    message = (
        f"<b>Привычка</b>  →  <i>{habit.action}</i>\n"
        f"<b>Место</b> →  <i>{habit.place or 'Не указано'}</i>\n"
        f"<b>Начало в</b>  →  <i>{habit.time.strftime('%H:%M')}</i>\n"
        f"<b>Время на выполнение</b>  →  <i>{habit.duration} секунд</i>\n"
        f"<b>Следующий раз</b>  →  <i>Через {next_time.get(habit.periodicity)}</i>\n"
    )

    if habit.reward:
        message += f"\n<b>Вознаграждение 🎁</b>  →  <i>{habit.reward}</i>"

    elif habit.related_habit:
        related = Habit.objects.get(id=habit.related_habit.id)
        message += (
            f"\n<b>Связанная привычка-вознаграждение 🎁</b>\n"
            f"<code>Занятие  →  {related.action}</code>\n"
            f"<code>Место  →  {related.place or 'Не указано'}</code>\n"
            f"<code>Начало в  →  {related.time.strftime('%H:%M')}</code>\n"
            f"<code>Время на выполнение  →  {related.duration} секунд</code>\n"
        )

    return message


def send_telegram_message(chat_id: str, message: str):
    """Отправляет сообщение в чат-бот Telegram."""
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    requests.get(f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage', params=params)


def get_today_send_time(habit: "Habit", now: datetime) -> datetime:
    habit_time = habit.time
    local_now = timezone.localtime(now)
    return local_now.replace(
        hour=habit_time.hour,
        minute=habit_time.minute,
        second=0,
        microsecond=0
    )


def revoke_and_clear_habit(habit: "Habit") -> None:
    """
    Отзывает запланированную задачу Celery,
    очищает поля task_id и next_notification и сохраняет изменения.
    """
    if habit.task_id:
        current_app.control.revoke(habit.task_id)
    habit.task_id = None
    habit.next_notification = None
    habit.save(update_fields=['task_id', 'next_notification'])


def schedule_habit_reminder(habit_id: str, force_revoke: bool = False) -> None:
    """
    Создаёт отложенную задачу для привычки.

    :arg habit_id: ID привычки
    :arg force_revoke: Сигнал для форсированного удаления старой задачи, срабатывает при ручном обновлении данных.
    """
    from habits.tasks import send_habit_reminder

    try:
        habit = Habit.objects.get(id=habit_id)
    except Habit.DoesNotExist:
        return

    chat_id = habit.user.telegram_chat_id
    if not chat_id:
        revoke_and_clear_habit(habit)
        return

    now = timezone.now()
    local_now = timezone.localtime(now)

    if not force_revoke:
        # Если уже есть активная задача и её время в будущем – завершаем операцию
        if habit.next_notification and habit.next_notification > local_now:
            print(f'Привычка {habit.pk} уже имеет актуальную задачу на уведомление')
            return

    # Удаление старой не актуальной задачи, если она была
    if habit.task_id:
        current_app.control.revoke(habit.task_id)
        print(f'Отзываем задачу {habit.task_id}')

    send_time = get_today_send_time(habit, local_now)

    if send_time <= local_now:
        # переносим на завтра
        send_time += timedelta(days=1)

    task = send_habit_reminder.apply_async((habit.pk,), eta=send_time)
    print(f'Запланирована привычка {habit.pk}: пользователь {habit.user}, время {send_time}')

    habit.task_id = task.id
    habit.next_notification = send_time
    habit.save(update_fields=['task_id', 'next_notification'])
