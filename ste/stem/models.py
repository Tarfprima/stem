# django.db.models - базовый модуль Django для работы с базой данных
# Содержит классы Model, CharField, ForeignKey и др. для описания структуры таблиц
# Без этого импорта: невозможно создавать модели, не работает ORM
from django.db import models

# django.contrib.auth.models.User - встроенная модель пользователя Django
# Предоставляет готовую систему авторизации с username, password, email
from django.contrib.auth.models import User

# random - стандартная библиотека Python для генерации случайных чисел
# Используется для создания уникальных 10-значных ID для Telegram интеграции
# Без этого импорта: не сможем генерировать уникальные коды для авторизации в боте
import random

# Модель Task для хранения заметок и напоминаний пользователей
class Task(models.Model):  # класс модели - наследуется от models.Model
    # Связь с пользователем - каждая задача принадлежит конкретному пользователю
    # on_delete=CASCADE означает, что при удалении пользователя удаляются и его задачи
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey - поле связи "многие к одному"
    
    # Название задачи (обязательное поле, максимум 200 символов)
    title = models.CharField(max_length=200)  # CharField - текстовое поле ограниченной длины
    
    # Описание задачи (необязательное поле, может быть пустым)
    description = models.TextField(blank=True)  # TextField - текстовое поле неограниченной длины; blank=True - может быть пустым
    
    # Время создания задачи (автоматически устанавливается при создании)
    created_at = models.DateTimeField(auto_now_add=True)  # DateTimeField - поле даты и времени; auto_now_add=True - автозаполнение при создании
    
    # Время напоминания (необязательное, используется только для напоминаний)
    reminder_time = models.DateTimeField(null=True, blank=True)  # null=True - может быть NULL в БД
    
    # Статус завершения задачи (по умолчанию False - не завершена)
    completed = models.BooleanField(default=False)  # BooleanField - булево поле True/False; default=False - значение по умолчанию
    
    # Статус просрочки задачи (по умолчанию False - не просрочена)
    overdue = models.BooleanField(default=False)  # булево поле для отметки просроченных задач
    
    # Статус отправки уведомления (для напоминаний через Telegram бота)
    notification_sent = models.BooleanField(default=False)  # булево поле отслеживания отправленных уведомлений
    
    # Строковое представление объекта (для отображения в админке и списках)
    def __str__(self):
        return self.title

# Модель для связывания пользователей сайта с Telegram ботом
class TelegramProfile(models.Model):  # класс модели профиля для Telegram интеграции
    # Связь один-к-одному с пользователем Django (у каждого пользователя один Telegram профиль)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # OneToOneField - поле связи "один к одному"
    
    # Уникальный 10-значный ID для авторизации в боте (генерируется автоматически)
    unique_id = models.BigIntegerField(unique=True, null=True, blank=True)  # BigIntegerField - поле для больших чисел; unique=True - уникальное значение
    
    # Chat ID из Telegram для отправки сообщений пользователю
    telegram_chat_id = models.BigIntegerField(null=True, blank=True)  # поле для хранения ID чата Telegram
    
    # Время создания профиля (автоматически устанавливается)
    connected_at = models.DateTimeField(auto_now_add=True)  # поле времени создания профиля
    
    def save(self, *args, **kwargs):  # метод save() - переопределение сохранения модели
        """Переопределяем метод save для автоматической генерации уникального ID"""
        # Генерируем уникальный 10-значный ID только при первом сохранении
        if not self.unique_id:  # проверка отсутствия ID
            while True:  # бесконечный цикл до получения уникального ID
                # Генерируем случайное 10-значное число
                unique_id = random.randint(1000000000, 9999999999)  # random.randint() - функция генерации случайного числа
                # Проверяем, что такого ID еще нет в базе
                if not TelegramProfile.objects.filter(unique_id=unique_id).exists():  # exists() - метод проверки существования объекта
                    self.unique_id = unique_id
                    break
        super().save(*args, **kwargs)  # super() - вызов родительского метода
    
    # Строковое представление объекта
    def __str__(self):
        return f"Telegram профиль {self.user.username}"