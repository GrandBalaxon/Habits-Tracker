from habits.serializers import HabitSerializer, PublicHabitSerializer
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
        serializer = HabitSerializer(data=data, context={'request': self.request})

        self.assertFalse(serializer.is_valid())
        self.assertIn("duration", serializer.errors)

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
        serializer = HabitSerializer(data=data, context={'request': self.request})

        self.assertFalse(serializer.is_valid())
        self.assertIn("periodicity", serializer.errors)

    def test_reward_and_related_habit_cannot_exist_together(self):
        """Нельзя одновременно указать вознаграждение и связанную привычку."""
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "duration": 60,
            "periodicity": 1,
            "action": "Учиться",
            "reward": "Сериал",
            "related_habit": self.pleasant_habit.id,
            "is_pleasant": False,
            "is_public": False,
            "notifications_on": False
        }
        serializer = HabitSerializer(data=data, context={'request': self.request})

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "Нельзя одновременно указать вознаграждение и связанную привычку",
            str(serializer.errors)
        )

    def test_related_habit_must_be_pleasant(self):
        """Связанная привычка должна быть приятной."""
        data = {
            "place": "Офис",
            "time": "08:00:00",
            "duration": 60,
            "periodicity": 1,
            "action": "Учиться",
            "related_habit": self.habit.id,
            "is_pleasant": False,
            "is_public": False,
            "notifications_on": False
        }
        serializer = HabitSerializer(data=data, context={'request': self.request})

        self.assertFalse(serializer.is_valid())
        self.assertIn("related_habit", serializer.errors)

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
        serializer = HabitSerializer(data=data, context={'request': self.request})

        self.assertFalse(serializer.is_valid())
        self.assertIn("У приятной привычки не может быть вознаграждения", str(serializer.errors))

    def test_public_habit_cannot_have_private_related_habit(self):
        """Публичная привычка не может иметь приватную связанную привычку."""
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "duration": 60,
            "periodicity": 1,
            "action": "Учиться",
            "related_habit": self.pleasant_habit.id,
            "is_pleasant": False,
            "is_public": True,
            "notifications_on": False
        }
        serializer = HabitSerializer(data=data, context={'request': self.request})

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
        serializer = HabitSerializer(data=data, context={'request': self.request})

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_duration_cannot_be_less_than_1_second(self):
        """Время выполнения не может быть меньше 1 секунды."""
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "duration": 0,
            "periodicity": 1,
            "action": "Тренировка",
            "is_pleasant": False,
            "reward": "Отдых",
            "is_public": False,
            "notifications_on": False
        }
        serializer = HabitSerializer(data=data, context={'request': self.request})

        self.assertFalse(serializer.is_valid())
        self.assertIn("duration", serializer.errors)

    def test_periodicity_cannot_be_less_than_1_day(self):
        """Периодичность не может быть меньше 1 дня."""
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "duration": 60,
            "periodicity": 0,
            "action": "Читать",
            "is_pleasant": False,
            "reward": None,
            "is_public": False,
            "notifications_on": False
        }
        serializer = HabitSerializer(data=data, context={'request': self.request})

        self.assertFalse(serializer.is_valid())
        self.assertIn("periodicity", serializer.errors)

    def test_pleasant_habit_cannot_have_related_habit(self):
        """Приятная привычка не может иметь связанную привычку."""
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "duration": 60,
            "periodicity": 1,
            "action": "Посмотреть сериал",
            "is_pleasant": True,
            "related_habit": self.pleasant_habit.id,
            "is_public": False,
            "notifications_on": False
        }
        serializer = HabitSerializer(data=data, context={'request': self.request})

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "У приятной привычки не может быть связанной привычки",
            str(serializer.errors)
        )

    def test_user_cannot_attach_foreign_habit(self):
        """Нельзя привязывать чужую привычку в качестве связанной."""
        # Создаем приятную привычку для ВТОРОГО пользователя
        foreign_pleasant_habit = Habit.objects.create(
            user=self.second_user,
            time="09:00:00",
            duration=60,
            periodicity=1,
            action="Чужая привычка",
            is_pleasant=True,
            is_public=True
        )

        data = {
            "place": "Дом",
            "time": "08:00:00",
            "duration": 60,
            "periodicity": 1,
            "action": "Учиться",
            "related_habit": foreign_pleasant_habit.id,
            "is_pleasant": False,
            "is_public": False,
            "notifications_on": False
        }
        serializer = HabitSerializer(data=data, context={'request': self.request})

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "Нельзя привязывать чужую привычку",
            str(serializer.errors)
        )

    def test_public_serializer_returns_public_related_habit(self):
        """PublicHabitSerializer возвращает данные, если связанная привычка публичная."""
        # Создаем публичную приятную привычку
        public_pleasant = Habit.objects.create(
            user=self.user, place="Дом", time="07:00:00", duration=60,
            periodicity=1, action="Публичная награда", is_pleasant=True, is_public=True
        )
        # Создаем публичную полезную привычку, привязанную к ней
        public_habit = Habit.objects.create(
            user=self.user, place="Дом", time="08:00:00", duration=60,
            periodicity=1, action="Полезное", is_pleasant=False, is_public=True,
            related_habit=public_pleasant
        )

        serializer = PublicHabitSerializer(public_habit)

        # Проверяем, что вернулся словарь
        self.assertIsInstance(serializer.data["related_habit"], dict)
        self.assertEqual(serializer.data["related_habit"]["id"], public_pleasant.id)
        self.assertEqual(serializer.data["related_habit"]["action"], "Публичная награда")
