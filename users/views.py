from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import CustomUser
from users.serializers import CustomUserSerializer


@extend_schema(tags=['Пользователь'], summary='Регистрация / Создание профиля')
class UserCreateApiView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


@extend_schema(
    tags=['Пользователь'],
    summary='Получение данных о пользователе',
    description='Авторизованный пользователь может посмотреть лишь данные своего профиля.'
)
class UserRetrieveApiView(RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(
    tags=['Пользователь'],
    summary='Обновление данных пользователя',
    description='Авторизованный пользователь может редактировать только данные своего профиля.'
)
class UserUpdateApiView(UpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(
    tags=['Пользователь'],
    summary='Удаление пользователя',
    description='Авторизованный пользователь может удалить только свой профиль.'
)
class UserDestroyApiView(DestroyAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
