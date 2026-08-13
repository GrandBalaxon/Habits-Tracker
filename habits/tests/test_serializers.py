from datetime import time

from habits.serializers import HabitSerializer
from habits.tests.base import BaseTestCase
from habits.models import Habit


class HabitSerializerTests(BaseTestCase):
    """Тесты сериализатора привычек."""

    def test_duration_cannot_be_more_than_120_seconds(self):
        """Время выполнения привычки не может быть больше 120 секунд."""
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "duration": 121,
            "periodicity": 1,
            "action": "Тренировка",
            "is_pleasant": False,
            "reward": "Отдых",
            "is_public": False,
            "notifications_on": False
        }
        serializer = HabitSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "duration",
            serializer.errors
        )

    def test_periodicity_cannot_be_more_than_7_days(self):
        """Периодичность привычки не может быть больше 7 дней."""
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "duration": 60,
            "periodicity": 8,
            "action": "Читать",
            "is_pleasant": False,
            "reward": None,
            "is_public": False,
            "notifications_on": False
        }
        serializer = HabitSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "periodicity",
            serializer.errors
        )

    def test_reward_and_related_habit_cannot_exist_together(self):
        """Нельзя одновременно указать вознаграждение и связанную привычку."""
        pleasant_habit = Habit.objects.create(
            user=self.user,
            time=time(7, 0),
            duration=60,
            periodicity=1,
            action="Выпить кофе",
            is_pleasant=True,
            is_public=False
        )
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "duration": 60,
            "periodicity": 1,
            "action": "Учиться",
            "reward": "Сериал",
            "related_habit": pleasant_habit.id,
            "is_pleasant": False,
            "is_public": False,
            "notifications_on": False
        }
        serializer = HabitSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "Нельзя одновременно указать вознаграждение и связанную привычку",
            str(serializer.errors)
        )

    def test_related_habit_must_be_pleasant(self):
        """Связанная привычка должна быть приятной."""
        normal_habit = Habit.objects.create(
            user=self.user,
            time=time(10, 0),
            duration=60,
            periodicity=1,
            action="Работать",
            is_pleasant=False,
            is_public=False
        )
        data = {
            "place": "Офис",
            "time": "08:00:00",
            "duration": 60,
            "periodicity": 1,
            "action": "Учиться",
            "related_habit": normal_habit.id,
            "is_pleasant": False,
            "is_public": False,
            "notifications_on": False
        }
        serializer = HabitSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "related_habit",
            serializer.errors
        )

    def test_pleasant_habit_cannot_have_reward(self):
        """Приятная привычка не может иметь вознаграждение."""
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "duration": 60,
            "periodicity": 1,
            "action": "Посмотреть сериал",
            "reward": "Купить игру",
            "is_pleasant": True,
            "is_public": False,
            "notifications_on": False
        }
        serializer = HabitSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "У приятной привычки не может быть вознаграждения",
            str(serializer.errors)
        )

    def test_public_habit_cannot_have_private_related_habit(self):
        """Публичная привычка не может иметь приватную связанную привычку."""
        private_pleasant_habit = Habit.objects.create(
            user=self.user,
            time=time(7, 0),
            duration=60,
            periodicity=1,
            action="Выпить чай",
            is_pleasant=True,
            is_public=False
        )
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "duration": 60,
            "periodicity": 1,
            "action": "Учиться",
            "related_habit": private_pleasant_habit.id,
            "is_pleasant": False,
            "is_public": True,
            "notifications_on": False
        }
        serializer = HabitSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "связанная привычка приватная",
            str(serializer.errors)
        )

    def test_valid_habit_is_created_successfully(self):
        """Корректная привычка успешно проходит сериализацию."""
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "duration": 60,
            "periodicity": 1,
            "action": "Читать книгу",
            "reward": "Отдых",
            "is_pleasant": False,
            "is_public": False,
            "notifications_on": False
        }
        serializer = HabitSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )
