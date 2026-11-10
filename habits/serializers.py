from typing import Any

from rest_framework import serializers

from habits.models import Habit


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор для публичных привычек."""
    related_habit = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = [
            'id',
            'action',
            'place',
            'time',
            'duration',
            'periodicity',
            'related_habit',
            'reward',
            'is_pleasant'
        ]

    def get_related_habit(self, obj):
        # Скрываем связанную привычку, если она приватная
        if obj.related_habit and obj.related_habit.is_public:
            return {
                'id': obj.related_habit.id,
                'action': obj.related_habit.action,
                'place': obj.related_habit.place,
                'time': obj.related_habit.time,
            }
        return None


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для собственных привычек."""

    class Meta:
        model = Habit
        fields = [
            'user',
            'place',
            'time',
            'duration',
            'periodicity',
            'action',
            'related_habit',
            'is_pleasant',
            'reward',
            'is_public',
            'notifications_on',
            'task_id',
            'next_notification'
        ]
        # Клиент не может менять создателя и внутренние поля Celery
        read_only_fields = ['user', 'task_id', 'next_notification']

    def validate_related_habit(self, value):
        if value:
            if not value.is_pleasant:
                raise serializers.ValidationError(
                    "В связанные привычки могут попадать только приятные привычки"
                )
            # Проверка на владельца: нельзя привязывать чужие привычки
            if value.user != self.context['request'].user:
                raise serializers.ValidationError("Нельзя привязывать чужую привычку")

        return value

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Валидирует итоговое состояние привычки перед сохранением.

        Для частичных обновлений (PATCH) объединяет новые данные из запроса с текущими значениями полей из экземпляра
        модели. Это предотвращает обход бизнес-правил, когда клиент меняет только одно поле, игнорируя несовместимые
        с ним существующие.
        """
        instance: Habit = self.instance

        def get_field(field_name: str, default: Any = None) -> Any:
            """
            Возвращает значение поля из входящих данных (data) или из существующего объекта базы данных (instance).
            """
            if field_name in data:
                return data[field_name]
            return getattr(instance, field_name, default) if instance else default

        is_pleasant = get_field('is_pleasant', False)
        reward = get_field('reward')
        related_habit = get_field('related_habit')
        is_public = get_field('is_public', False)

        # 1. Исключить одновременный выбор связанной привычки и указания вознаграждения
        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя одновременно указать вознаграждение и связанную привычку"
            )

        # 2. У приятной привычки не может быть вознаграждения или связанной привычки
        if is_pleasant:
            if reward:
                raise serializers.ValidationError(
                    "У приятной привычки не может быть вознаграждения"
                )
            if related_habit:
                raise serializers.ValidationError(
                    "У приятной привычки не может быть связанной привычки"
                )

        # 3. Если привычка публичная и имеет связанную привычку, связанная привычка тоже должна быть публичной
        if is_public and related_habit:
            if not related_habit.is_public:
                raise serializers.ValidationError(
                    "Нельзя сделать привычку публичной, если связанная привычка приватная. "
                    "Сначала сделайте связанную привычку публичной."
                )

        return data
