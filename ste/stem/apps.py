# django.apps.AppConfig - базовый класс для конфигурации Django приложений
# Определяет настройки приложения: название, тип первичного ключа, готовность к работе
# Без этого импорта: приложение не может быть корректно инициализировано Django
from django.apps import AppConfig


class StemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stem'
