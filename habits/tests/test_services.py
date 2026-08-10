from datetime import time

from django.utils import timezone
from unittest.mock import patch, MagicMock

from habits.models import Habit
from habits.services import (
    make_telegram_habit_message,
    send_telegram_message,
    get_today_send_time,
    revoke_and_clear_habit,
    schedule_habit_reminder,
)

from habits.tests.base import BaseTestCase


class TelegramMessageTests(BaseTestCase):
    """Тесты генерации Telegram сообщений."""

    def test_message_contains_habit_information(self):
        """Сообщение содержит основные данные привычки."""
        message = make_telegram_habit_message(self.habit)

        self.assertIn(self.habit.action, message)
        self.assertIn(self.habit.place, message)
        self.assertIn(str(self.habit.duration), message)
        self.assertIn(self.habit.reward, message)


    def test_message_contains_related_habit(self):
        """Сообщение содержит связанную привычку."""
        related = Habit.objects.create(
            user=self.user,
            action="Выпить кофе",
            time=time(8, 0),
            duration=60,
            periodicity=1,
            is_pleasant=True,
            is_public=False
        )

        self.habit.reward = None
        self.habit.related_habit = related
        self.habit.save()

        message = make_telegram_habit_message(self.habit)

        self.assertIn(
            related.action,
            message
        )


class TelegramSendTests(BaseTestCase):
    """Тесты отправки сообщений Telegram."""

    @patch("habits.services.requests.get")
    def test_send_telegram_message_calls_api(self,mock_get):
        """
        Функция отправляет запрос в Telegram API.
        """
        send_telegram_message("12345","Тестовое сообщение")

        mock_get.assert_called_once()

        _, kwargs = mock_get.call_args

        self.assertEqual(
            kwargs["params"]["chat_id"],
            "12345"
        )
        self.assertEqual(
            kwargs["params"]["text"],
            "Тестовое сообщение"
        )
        self.assertEqual(
            kwargs["params"]["parse_mode"],
            "HTML"
        )


class HabitTimeTests(BaseTestCase):
    """Тесты расчёта времени уведомления."""


    def test_get_today_send_time_returns_habit_time(self):
        """Время уведомления берётся из привычки."""
        now = timezone.now()

        result = get_today_send_time(self.habit, now)
        self.assertEqual(result.hour, self.habit.time.hour)
        self.assertEqual(result.minute, self.habit.time.minute)


class RevokeHabitTests(BaseTestCase):
    """Тесты удаления задач Celery."""

    @patch("habits.services.current_app.control.revoke")
    def test_revoke_and_clear_habit_removes_task(self, mock_revoke):
        """Старая задача отзывается и очищается."""

        Habit.objects.filter(id=self.habit.id).update(
            task_id="old-task-id",
            next_notification=timezone.now()
        )
        self.habit.refresh_from_db()

        revoke_and_clear_habit(self.habit)

        mock_revoke.assert_called_once_with("old-task-id")

        self.habit.refresh_from_db()

        self.assertIsNone(self.habit.task_id)
        self.assertIsNone(self.habit.next_notification)


class ScheduleHabitTests(BaseTestCase):
    """Тесты планирования уведомлений."""

    @patch("habits.tasks.send_habit_reminder.apply_async")
    def test_schedule_creates_celery_task(self, mock_apply_async):
        """Создаётся задача Celery."""

        self.user.telegram_chat_id = "12345"
        self.user.save()

        Habit.objects.filter(id=self.habit.id).update(notifications_on=True)

        mock_task = MagicMock()
        mock_task.id = "new-task-id"

        mock_apply_async.return_value = mock_task

        schedule_habit_reminder(self.habit.id)

        mock_apply_async.assert_called_once()

        self.habit.refresh_from_db()

        self.assertEqual(self.habit.task_id, "new-task-id")
        self.assertIsNotNone(self.habit.next_notification)


    @patch("habits.tasks.send_habit_reminder.apply_async")
    def test_schedule_does_not_create_duplicate_task(self, mock_apply_async):
        """Если задача уже актуальна, новая не создаётся."""
        self.user.telegram_chat_id = "12345"
        self.user.save()

        Habit.objects.filter(id=self.habit.id).update(
            notifications_on = True,
            next_notification = timezone.now() + timezone.timedelta(days=1)
        )

        schedule_habit_reminder(self.habit.id)
        mock_apply_async.assert_not_called()


    @patch("habits.services.revoke_and_clear_habit")
    def test_schedule_clears_task_when_notifications_disabled(self, mock_revoke):
        """При выключенных уведомлениях задача удаляется."""

        Habit.objects.filter(id=self.habit.id).update(
            notifications_on=False,
            task_id="old-task"
        )

        schedule_habit_reminder(self.habit.id)
        mock_revoke.assert_called_once()
