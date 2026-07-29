from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.pagination import FiveElementsPagination
from habits.serializers import HabitSerializer, PublicHabitSerializer


@extend_schema(
    tags=['Привычки'],
    summary='Список общедоступных привычек',
    description='Любой авторизованный пользователь может просматривать публичные привычки других пользователей.'
)
class HabitsListApiView(ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = FiveElementsPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).exclude(user=self.request.user)


@extend_schema(
    tags=['Привычки'],
    summary='Детали привычки',
    description='Пользователь может посмотреть детали своей привычки или любой публичной привычки.'
)
class HabitRetrieveApiView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(
                    Q(user=self.request.user) | Q(is_public=True)
                )

    def get_serializer_class(self):
        habit = self.get_object()
        if habit.is_public and habit.user != self.request.user:
            return PublicHabitSerializer
        return HabitSerializer


@extend_schema(
    tags=['Привычки'],
    summary='Создание привычки'
)
class HabitCreateApiView(CreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    tags=['Привычки'],
    summary='Обновление привычки',
    description='Авторизованный пользователь может редактировать только свои привычки.'
)
class HabitUpdateApiView(UpdateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


@extend_schema(
    tags=['Привычки'],
    summary='Удаление привычки',
    description='Авторизованный пользователь может удалить только свои привычки.'
)
class HabitDestroyApiView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)