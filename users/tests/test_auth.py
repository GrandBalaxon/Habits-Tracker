from django.urls import reverse
from rest_framework.test import APITestCase

from users.models import CustomUser


class CustomUserManagerTests(APITestCase):
    """Тесты кастомного менеджера пользователей."""

    def test_create_user_raises_error_without_email(self):
        """Создание пользователя без email вызывает ValueError."""
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email="", password="12345")

    def test_create_superuser_raises_error_with_wrong_flags(self):
        """Создание суперюзера с неверными флагами вызывает ValueError."""
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(email="admin@test.ru", password="12345", is_staff=False)

        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(email="admin2@test.ru", password="12345", is_superuser=False)


class UserSerializerTests(APITestCase):
    """Тесты создания и обновления пользователя (покрытие create/update)."""

    @classmethod
    def setUpTestData(cls):
        cls.create_url = reverse("users:create")
        cls.update_url = reverse("users:update")
        cls.user = CustomUser.objects.create_user(email="test@test.ru", password="OldPassword123!")

    def login_user(self) -> None:
        self.client.force_authenticate(self.user)

    def test_create_user_via_api(self):
        """Регистрация создает пользователя с хэшированным паролем."""
        data = {"email": "new@test.ru", "password": "NewPassword123!"}
        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(response.status_code, 201)
        user = CustomUser.objects.get(email="new@test.ru")
        self.assertTrue(user.check_password("NewPassword123!"))

    def test_update_user_password(self):
        """Обновление пароля через PATCH."""
        self.login_user()
        data = {"password": "BrandNewPassword123!"}
        response = self.client.patch(self.update_url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("BrandNewPassword123!"))

    def test_update_user_without_password(self):
        """Обновление профиля без пароля не ломает старый пароль."""
        self.login_user()
        data = {"username": "newname"}
        response = self.client.patch(self.update_url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "newname")
        self.assertTrue(self.user.check_password("OldPassword123!"))
