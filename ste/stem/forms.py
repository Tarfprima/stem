from django import forms
from . models import Task #Task это класс из models.py

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'reminder_time']
        widgets = {'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})}, #'datetime-local' это я использую для удобного выбора времени.
        labels = {
            'title': 'Название задачи',
            'description': 'Описание',
            'reminder_time': 'Время напоминания',
        }

