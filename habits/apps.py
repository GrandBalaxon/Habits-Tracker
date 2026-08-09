from django.apps import AppConfig


class HabitsConfig(AppConfig):
    name = "habits"
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        # Импорт сигналов, чтобы они были зарегистрированы
        import habits.signals
