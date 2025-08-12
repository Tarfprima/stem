# Импортируем модули Django для создания модели
from django.db import models
from django.contrib.auth.models import User  # Импортируем встроенную модель User для связи с пользователем
from datetime import datetime  # Импортируем datetime для автоматической установки времени создания

# Создаём модель Task для хранения заметок и напоминаний
class Task(models.Model):
    # Поле для связи с пользователем — используем ForeignKey, чтобы каждая задача была привязана к пользователю
    # on_delete=models.CASCADE означает, что если пользователь удалён, его задачи тоже удаляются 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Название задачи — короткий текст (до 200 символов)
    title = models.CharField(max_length=200)

    # Описание —  длинный текст
    description = models.TextField(blank=True)

    # Время создания — автоматически заполняется при добавлении (auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Время напоминания — (null=True), используется для напоминаний
    reminder_time = models.DateTimeField(null=True, blank=True)

    # Статус завершения — булевое поле, по умолчанию False (не завершено)
    completed = models.BooleanField(default=False)
    
    # Магический метод __str__ — возвращает название задачи для удобного отображения в админке и списке
    def __str__(self):
        return self.title
    
    # auto_now_add=True — автоматически ставит текущую дату при создании записи, не требует ручного заполнения.
    # blank=True и null=True — делают поле необязательным для форм и базы данных (blank для форм, null для базы).