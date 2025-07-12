from django.db import models
from datetime import datetime
from django.contrib.auth.models import User # Возможность дабавить пользователя 

# Ранний models.py 
class Task(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE) # Добавление пользователя и условия для удаления всех данных.
    name = models.CharField(max_length=255) # заголовок 
    description = models.CharField(max_length=10000) # текстовое поле
    created = models.DateTimeField(default=datetime.now(), blank=True) # Поле даты
    

    def __str__(self):
        return self.name    