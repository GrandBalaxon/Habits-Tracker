from django.urls import reverse

from habits.models import Habit
from habits.tests.base import BaseTestCase


class HabitTests(BaseTestCase):
    """Тесты вьюх для модели привычек."""

    # --- Создание ---

    def test_authenticated_user_can_create_habit(self):
        """Авторизованный пользователь может создать привычку."""
        self.login_user()

        data = {
            "place": "Офис",
            "time": "08:00:00",
            "duration": 30,
            "periodicity": 1,
            "action": "Работать",
            "is_pleasant": False,
            "reward": "Кофе",
            "is_public": False,
            "notifications_on": False
        }

        response = self.client.post(self.create_url, data=data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["user"], self.user.id)

        # Проверяем, что запись реально создалась в БД
        self.assertTrue(Habit.objects.filter(action="Работать", user=self.user).exists())

    def test_unauthenticated_user_cannot_create_habit(self):
        """Неавторизованный пользователь не может создать привычку."""
        self.logout()
        response = self.client.post(self.create_url, {}, format='json')

        self.assertEqual(response.status_code, 401)

    # --- Чтение ---

    def test_user_can_get_public_habits(self):
        """Пользователь может получить список публичных привычек."""
        self.login_user()

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data["results"]), 1)

    def test_private_habits_are_not_in_public_list(self):
        """Приватные привычки не отображаются в публичном списке."""
        self.login_user()

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        actions = [habit["action"] for habit in data["results"]]
        self.assertNotIn(self.private_habit.action, actions)

    def test_owner_can_get_habit(self):
        """Владелец может получить свою привычку."""
        self.login_user()

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)

    def test_user_can_get_public_habit(self):
        """Пользователь может получить чужую публичную привычку."""
        self.login_user()

        url = reverse("habits:detail", kwargs={"pk": self.public_habit.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_user_cannot_get_private_habit_of_other_user(self):
        """Пользователь не может получить чужую приватную привычку."""
        self.login_user()

        url = reverse("habits:detail", kwargs={"pk": self.private_habit.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    # --- Обновление ---

    def test_owner_can_update_habit(self):
        """Пользователь может изменить свою привычку."""
        self.login_user()

        response = self.client.patch(
            self.update_url,
            data={"action": "Бегать"},
            format='json'
        )

        self.assertEqual(response.status_code, 200)

        # Проверяем, что данные реально обновились в БД
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Бегать")

    def test_user_cannot_update_other_user_habit(self):
        """Пользователь не может изменить чужую привычку."""
        self.login_user()

        url = reverse("habits:update", kwargs={"pk": self.private_habit.id})
        response = self.client.patch(
            url,
            data={"action": "Новое действие"},
            format='json'
        )

        self.assertEqual(response.status_code, 404)

    # --- Удаление ---

    def test_owner_can_delete_habit(self):
        """Пользователь может удалить свою привычку."""
        self.login_user()

        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, 204)

        # Проверяем, что запись удалена из БД
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())

    def test_user_cannot_delete_other_user_habit(self):
        """Пользователь не может удалить чужую привычку."""
        self.login_user()

        url = reverse("habits:delete", kwargs={"pk": self.private_habit.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)

        # Проверяем, что запись осталась в БД
        self.assertTrue(Habit.objects.filter(id=self.private_habit.id).exists())
