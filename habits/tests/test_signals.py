from unittest.mock import patch

from habits.tests.base import BaseTestCase


@patch("habits.signals.transaction.on_commit", side_effect=lambda func: func())
class HabitSignalTests(BaseTestCase):
    """Тесты сигналов Django."""

    @patch("habits.services.schedule_habit_reminder")
    def test_post_save_schedules_task_on_notifications_on(self, mock_schedule, mock_on_commit):
        """При создании/обновлении с уведомлениями вызывается планировщик."""
        self.habit.notifications_on = True
        self.habit.save()

        mock_schedule.assert_called_once_with(self.habit.id, force_revoke=True)

    @patch("habits.services.schedule_habit_reminder")
    @patch("habits.signals.logger.error")
    def test_post_save_logs_error_if_scheduler_fails(self, mock_logger, mock_schedule, mock_on_commit):
        """Если планировщик падает, ошибка логируется (а не ломает API)."""
        self.habit.notifications_on = True
        mock_schedule.side_effect = Exception("Broker is down")

        # Не должно вызвать ошибку
        self.habit.save()

        mock_logger.assert_called_once()
        self.assertIn("Broker is down", mock_logger.call_args[0][0])

    @patch("habits.signals.current_app.control.revoke")
    def test_post_save_revokes_task_when_notifications_disabled(self, mock_revoke, mock_on_commit):
        """Если уведомления выключаются, старая задача отзывается."""
        self.habit.notifications_on = False
        self.habit.task_id = "old-task-id"
        self.habit.save()

        mock_revoke.assert_called_once_with("old-task-id")

    @patch("habits.signals.current_app.control.revoke")
    def test_pre_delete_revokes_task(self, mock_revoke, mock_on_commit):
        """При удалении привычки задача отзывается."""
        self.habit.task_id = "task-to-delete"
        self.habit.delete()

        mock_revoke.assert_called_once_with("task-to-delete")

    @patch("habits.signals.current_app.control.revoke")
    @patch("habits.signals.logger.error")
    def test_post_save_logs_error_if_revoke_fails(self, mock_logger, mock_revoke, mock_on_commit):
        """Если при отзыве задачи Celery падает ошибка, она логируется."""
        self.habit.notifications_on = False
        self.habit.task_id = "old-task-id"

        # Имитируем падение Celery
        mock_revoke.side_effect = Exception("Celery connection error")

        # Сохраняем привычку (сигнал post_save сработает, вызовет on_commit,
        # а тот попытается отозвать задачу и упадет)
        self.habit.save()

        # Проверяем, что ошибка была перехвачена и залогирована
        mock_logger.assert_called_once()
        self.assertIn("Celery connection error", mock_logger.call_args[0][0])
