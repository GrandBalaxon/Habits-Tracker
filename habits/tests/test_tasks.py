from unittest.mock import patch, MagicMock

from habits.tasks import send_habit_reminder, set_up_all_reminders
from habits.tests.base import BaseTestCase


class HabitTasksTests(BaseTestCase):
    """Тесты Celery-задач."""

    @patch("habits.tasks.send_telegram_message")
    @patch("habits.tasks.send_habit_reminder.apply_async")
    def test_send_habit_reminder_success(self, mock_apply_async, mock_send_tg):
        """Успешная отправка и планирование следующей задачи."""
        self.user.telegram_chat_id = "12345"
        self.user.save()

        self.habit.notifications_on = True
        self.habit.save()

        # Мокаем возвращаемое значение для новой задачи
        mock_task = MagicMock()
        mock_task.id = "next-task-id"
        mock_apply_async.return_value = mock_task

        # Вызываем задачу напрямую (как будто Celery её запустил)
        send_habit_reminder(self.habit.id)

        mock_send_tg.assert_called_once()
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.task_id, "next-task-id")

    @patch("habits.tasks.revoke_and_clear_habit")
    def test_send_habit_reminder_no_chat_id(self, mock_revoke):
        """Если у пользователя нет chat_id, задача отменяется."""
        self.user.telegram_chat_id = None
        self.user.save()

        self.habit.notifications_on = True
        self.habit.task_id = "some-task"
        self.habit.save()

        send_habit_reminder(self.habit.id)
        mock_revoke.assert_called_once()

    @patch("habits.tasks.schedule_habit_reminder")
    def test_set_up_all_reminders(self, mock_schedule):
        """Задача находит всех пользователей с chat_id и планирует уведомления."""
        self.user.telegram_chat_id = "12345"
        self.user.save()

        set_up_all_reminders()

        # У self.user теперь две привычки: self.habit и self.pleasant_habit
        self.assertEqual(mock_schedule.call_count, 2)

        # Проверяем, что вызовы были именно для его привычек
        mock_schedule.assert_any_call(self.habit.id)
        mock_schedule.assert_any_call(self.pleasant_habit.id)

    @patch("habits.tasks.send_habit_reminder.apply_async")
    def test_send_habit_reminder_habit_not_found(self, mock_apply_async):
        """Если привычки нет в БД, логируется предупреждение и задача не создается."""
        with self.assertLogs("habits.tasks", level="WARNING") as cm:
            send_habit_reminder(999999)

        self.assertIn("Привычка 999999 не найдена", cm.output[0])
        mock_apply_async.assert_not_called()
