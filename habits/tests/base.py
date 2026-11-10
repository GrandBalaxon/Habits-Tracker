from datetime import time

from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from habits.models import Habit
from users.models import CustomUser


class BaseTestCase(APITestCase):
    """Базовый класс с общими тестовыми данными."""

    @classmethod
    def setUpTestData(cls):
        # ---------- Пользователи ----------
        cls.user = CustomUser.objects.create_user(
            email="user@test.ru",
            password="12345"
        )
        cls.second_user = CustomUser.objects.create_user(
            email="second@test.ru",
            password="12345"
        )

        # Создаем фейковый запрос от лица cls.user
        cls.factory = APIRequestFactory()
        cls.request = cls.factory.get('/')
        cls.request.user = cls.user

        # ---------- Привычки ----------
        cls.habit = Habit.objects.create(
            user=cls.user,
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
        cls.public_habit = Habit.objects.create(
            user=cls.second_user,
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
        cls.private_habit = Habit.objects.create(
            user=cls.second_user,
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
        cls.pleasant_habit = Habit.objects.create(
            user=cls.user,
            place="Диван",
            time=time(20, 0),
            duration=30,
            periodicity=1,
            action="Смотреть сериал",
            is_pleasant=True,
            is_public=False,
            notifications_on=False
        )

        # ---------- URL-ы ----------
        cls.list_url = reverse("habits:list")
        cls.create_url = reverse("habits:create")
        cls.detail_url = reverse("habits:detail", kwargs={"pk": cls.habit.id})
        cls.update_url = reverse("habits:update", kwargs={"pk": cls.habit.id})
        cls.delete_url = reverse("habits:delete", kwargs={"pk": cls.habit.id})


    # ---------- Хелперы: аутентификация ----------
    def login_user(self) -> None:
        self.client.force_authenticate(self.user)

    def login_second_user(self) -> None:
        self.client.force_authenticate(self.second_user)

    def logout(self) -> None:
        """Сбросить аутентификацию клиента."""
        self.client.force_authenticate(None)
