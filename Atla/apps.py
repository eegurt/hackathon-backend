from django.apps import AppConfig


class AtlaConfig(AppConfig):
    name = 'Atla'

    def ready(self):
        # Подключаем сигналы для автоматического пересчёта приоритета
        import Atla.signals  # noqa: F401
