import requests

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
        7: "7 дней"
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


def send_telegram_message(chat_id, message):
    """Отправляет сообщение в чат-бот Telegram."""
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    requests.get(f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage', params=params)
