"""
ASGI config for ste project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# os - встроенная библиотека Python для работы с операционной системой  
# Используется для установки переменной окружения DJANGO_SETTINGS_MODULE
# Без этого импорта: ASGI сервер не сможет найти настройки Django проекта
import os

# django.core.asgi.get_asgi_application - функция создания ASGI приложения
# Создает ASGI callable для асинхронных функций и WebSocket соединений
# Без этого импорта: невозможно использовать асинхронные возможности Django и WebSocket
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ste.settings')

application = get_asgi_application()
