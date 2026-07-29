from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    habits_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "habits_count"]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'validators': [
                    UniqueValidator(
                        queryset=CustomUser.objects.all(),
                        message="Пользователь с таким email уже существует."
                    )
                ]
            }
        }

    def get_habits_count(self, obj):
        return obj.habits.count()

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
