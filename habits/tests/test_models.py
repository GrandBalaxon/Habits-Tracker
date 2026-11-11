from django.core.exceptions import ValidationError
from habits.tests.base import BaseTestCase


class HabitModelTests(BaseTestCase):
    """Тесты модели привычки (валидация clean и str)."""

    def test_str_representation(self):
        """Строковое представление возвращает корректный формат."""
        expected = f"Я буду {self.habit.action} в {self.habit.time} в {self.habit.place}"
        self.assertEqual(str(self.habit), expected)

    def test_clean_success(self):
        """Валидация проходит успешно для корректных данных."""
        try:
            self.habit.clean()
        except ValidationError as e:
            self.fail(f"Метод clean() выбросил неожиданную ошибку валидации: {e}")

    def test_clean_raises_on_pleasant_with_reward(self):
        """Приятная привычка не может иметь вознаграждение."""
        self.habit.is_pleasant = True
        self.habit.reward = "Конфета"

        with self.assertRaises(ValidationError):
            self.habit.clean()

    def test_clean_raises_on_pleasant_with_related_habit(self):
        """Приятная привычка не может иметь связанную привычку."""
        self.habit.is_pleasant = True
        self.habit.reward = None
        self.habit.related_habit = self.pleasant_habit

        with self.assertRaises(ValidationError):
            self.habit.clean()

    def test_clean_raises_on_reward_and_related_habit(self):
        """Нельзя одновременно указывать вознаграждение и связанную привычку."""
        self.habit.is_pleasant = False
        self.habit.reward = "Конфета"
        self.habit.related_habit = self.pleasant_habit

        with self.assertRaises(ValidationError):
            self.habit.clean()

    def test_clean_raises_on_long_duration(self):
        """Время выполнения не может быть больше 120 секунд."""
        self.habit.duration = 130

        with self.assertRaises(ValidationError):
            self.habit.clean()
