
from django.contrib import admin

# Импорт модели Task из текущего приложения  
# Используется для регистрации модели в административном интерфейсе
# Без этого импорта: модель Task не будет доступна в админ-панели для управления
from .models import Task

# Регистрируем модель Task с помощью декоратора 
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке в админке
    list_display = ['title', 'user', 'created_at', 'completed', 'reminder_time']