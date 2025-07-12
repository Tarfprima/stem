from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # Возможность дабавить пользователя 


class Task(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE) # Добавление пользователя и условия для удаления всех данных.
    name = models.CharField(max_length=255) # заголовок 
    description = models.CharField(max_length=10000) # текстовое поле
    created = models.DateTimeField(default=timezone.now, blank=True) # поле даты
    

    def __str__(self):
        return self.name    