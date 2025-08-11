from django.db import models
from datetime import datetime
from django.contrib.auth.models import User # Возможность дабавить пользователя 

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    reminder_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    # Поля: title, description, reminder_time, created_at, completed.
    # user: Привязка задачи к пользователю через ForeignKey.
    # completed: Булево поле для статуса задачи