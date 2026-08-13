from datetime import time

from django.urls import reverse
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import CustomUser


class BaseTestCase(APITestCase):
    """Базовый класс с общими тестовыми данными."""

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="user@test.ru",
            password="12345"
        )

        self.second_user = CustomUser.objects.create_user(
            email="second@test.ru",
            password="12345"
        )

        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time=time(9, 0),
            duration=60,
            periodicity=1,
            action="Читать книгу",
            is_pleasant=False,
            reward="Посмотреть сериал",
            is_public=False,
            notifications_on=False
        )

        self.public_habit = Habit.objects.create(
            user=self.second_user,
            place="Парк",
            time=time(10, 0),
            duration=60,
            periodicity=1,
            action="Гулять",
            is_pleasant=False,
            reward=None,
            is_public=True,
            notifications_on=False
        )

        self.private_habit = Habit.objects.create(
            user=self.second_user,
            place="Дом",
            time=time(12, 0),
            duration=60,
            periodicity=1,
            action="Учиться",
            is_pleasant=False,
            reward=None,
            is_public=False,
            notifications_on=False
        )

        self.list_url = reverse("habits:list")
        self.create_url = reverse("habits:create")
        self.detail_url = reverse(
            "habits:detail",
            kwargs={"pk": self.habit.id}
        )
        self.update_url = reverse(
            "habits:update",
            kwargs={"pk": self.habit.id}
        )
        self.delete_url = reverse(
            "habits:delete",
            kwargs={"pk": self.habit.id}
        )
