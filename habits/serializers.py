from rest_framework import serializers

from habits.models import Habit


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор для публичных привычек."""
    related_habit = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = [
            'id', 'action', 'place', 'time', 'duration',
            'periodicity', 'related_habit', 'reward', 'is_pleasant'
        ]

    def get_related_habit(self, obj):
        if obj.related_habit:
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
        fields = '__all__'

    @staticmethod
    def validate_duration(value):
        if value > 120:
            raise serializers.ValidationError(
                "Время выполнения должно быть не больше 120 секунд"
            )
        return value

    @staticmethod
    def validate_periodicity(value):
        if value > 7:
            raise serializers.ValidationError(
                "Нельзя выполнять привычку реже, чем 1 раз в 7 дней"
            )
        return value

    @staticmethod
    def validate_related_habit(value):
        if value and not value.is_pleasant:
            raise serializers.ValidationError(
                "В связанные привычки могут попадать только привычки с признаком приятной"
            )
        return value

    def validate(self, data):
        # Исключить одновременный выбор связанной привычки и указания вознаграждения
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError(
                "Нельзя одновременно указать вознаграждение и связанную привычку"
            )

        # У приятной привычки не может быть вознаграждения или связанной привычки
        if data.get('is_pleasant'):
            if data.get('reward'):
                raise serializers.ValidationError(
                    "У приятной привычки не может быть вознаграждения"
                )
            if data.get('related_habit'):
                raise serializers.ValidationError(
                    "У приятной привычки не может быть связанной привычки"
                )

        # Если привычка публичная и имеет связанную привычку, связанная привычка тоже должна быть публичной
        if data.get('is_public') and data.get('related_habit'):
            if not data['related_habit'].is_public:
                raise serializers.ValidationError(
                    "Нельзя сделать привычку публичной, если связанная привычка приватная. "
                    "Сначала сделайте связанную привычку публичной."
                )

        return data
