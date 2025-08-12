# Импортируем модуль admin для регистрации модели в админке
from django.contrib import admin
# Импортируем модель Task
from .models import Task

# Регистрируем модель Task с помощью декоратора 
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке в админке
    list_display = ['title', 'user', 'created_at', 'completed', 'reminder_time']