from django.urls import reverse

from habits.models import Habit
from users.models import CustomUser
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    """Тесты вьюх для модели пользователя."""

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="test@test.ru",
            password="strong_password123"
        )
        cls.profile_url = reverse("users:profile")
        cls.update_url = reverse("users:update")
        cls.create_url = reverse("users:create")

    def login_user(self):
        self.client.force_authenticate(self.user)

    # --- Чтение профиля ---

    def test_user_can_view_own_profile(self):
        """Пользователь может посмотреть свой профиль."""
        self.login_user()
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], self.user.email)

    def test_user_can_get_own_habits_list(self):
        """Пользователь может получить список только своих привычек."""
        self.login_user()

        # Создаем привычку для текущего пользователя
        my_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            duration=10,
            periodicity=1,
            action="Моя привычка",
            is_pleasant=False
        )

        url = reverse("users:user-habits")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Проверяем, что вернулась именно наша привычка
        data = response.json()
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["action"], "Моя привычка")

    # --- Обновление профиля ---

    def test_user_can_update_telegram_chat_id(self):
        """Пользователь может привязать telegram_chat_id."""
        self.login_user()
        response = self.client.patch(
            self.update_url,
            data={"telegram_chat_id": "987654321"},
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.telegram_chat_id, "987654321")

    # --- Регистрация ---

    def test_registration_with_weak_password_fails(self):
        """Регистрация с паролем из 1 символа должна упасть."""
        data = {"email": "new@test.ru", "password": "1"}

        response = self.client.post(self.create_url, data=data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.json())

    # --- Удаление ---

    def test_user_can_delete_own_profile(self):
        """Пользователь может удалить свой профиль."""
        self.login_user()
        delete_url = reverse("users:destroy")

        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 204)
        # Проверяем, что пользователь реально удален из БД
        self.assertFalse(CustomUser.objects.filter(id=self.user.id).exists())
