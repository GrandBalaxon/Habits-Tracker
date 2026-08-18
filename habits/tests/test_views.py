from unittest.mock import patch

from django.urls import reverse
from rest_framework import status

from habits.tests.base import BaseTestCase


class HabitCreateTests(BaseTestCase):
    """Тесты создания привычек."""

    @patch("habits.models.Habit.save")
    def test_authenticated_user_can_create_habit(self, mock_save):
        """Авторизованный пользователь может создать привычку."""

        self.client.force_authenticate(
            user=self.user
        )

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

        response = self.client.post(
            self.create_url,
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data["user"],
            self.user.id
        )

    def test_unauthenticated_user_cannot_create_habit(self):
        """Неавторизованный пользователь не может создать привычку."""

        response = self.client.post(
            self.create_url,
            {}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class HabitListTests(BaseTestCase):
    """Тесты получения списка привычек."""

    def test_user_can_get_public_habits(self):
        """Пользователь может получить список публичных привычек."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data["results"]),
            1
        )

    def test_private_habits_are_not_in_public_list(self):
        """Приватные привычки не отображаются в публичном списке."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)

        self.assertNotIn(
            self.private_habit.action,
            [
                habit["action"]
                for habit in response.data["results"]
            ]
        )


class HabitRetrieveTests(BaseTestCase):
    """Тесты получения одной привычки."""

    def test_owner_can_get_habit(self):
        """Владелец может получить свою привычку."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_user_can_get_public_habit(self):
        """Пользователь может получить чужую публичную привычку."""
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:detail", kwargs={"pk": self.public_habit.id})
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_user_cannot_get_private_habit_of_other_user(self):
        """Пользователь не может получить чужую приватную привычку."""
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:detail", kwargs={"pk": self.private_habit.id})
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )


class HabitUpdateTests(BaseTestCase):
    """Тесты обновления привычек."""

    @patch("habits.models.Habit.save")
    def test_owner_can_update_habit(self, mock_save):
        """Пользователь может изменить свою привычку."""
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            self.update_url,
            {
                "action": "Бегать"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_user_cannot_update_other_user_habit(self):
        """Пользователь не может изменить чужую привычку."""
        self.client.force_authenticate(user=self.user)

        url = reverse(
            "habits:update",
            kwargs={"pk": self.private_habit.id}
        )

        response = self.client.patch(
            url,
            {
                "action": "Новое действие"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )


class HabitDeleteTests(BaseTestCase):
    """Тесты удаления привычек."""

    def test_owner_can_delete_habit(self):
        """Пользователь может удалить свою привычку."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.delete_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_user_cannot_delete_other_user_habit(self):
        """Пользователь не может удалить чужую привычку."""
        self.client.force_authenticate(user=self.user)

        url = reverse(
            "habits:delete",
            kwargs={"pk": self.private_habit.id}
        )
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
