from rest_framework import serializers

from habits.models import Habit


class HabitsSerializer(serializers.ModelSerializer):
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

        return data
