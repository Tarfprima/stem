# django.forms - модуль Django для создания HTML форм и их валидации
# Предоставляет классы Form, ModelForm, CharField, TextInput и другие виджеты
# Без этого импорта: невозможно создавать веб-формы, нет валидации пользовательского ввода
from django import forms

# Импорт нашей модели Task из текущего приложения
# Используется для создания ModelForm - форм, автоматически связанных с моделью
# Без этого импорта: нельзя создавать формы для создания/редактирования задач
from .models import Task

# Форма для добавления заметки (без времени)
class NoteForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настройка заголовков полей
        self.fields['title'].label = 'Название заметки'
        self.fields['description'].label = 'Описание'
        
        # Настройка внешнего вида полей
        self.fields['title'].widget = forms.TextInput(attrs={'placeholder': 'Введите название'})
        self.fields['description'].widget = forms.Textarea(attrs={'placeholder': 'Введите описание', 'rows': 4})

# Форма для добавления напоминания (с обязательным временем)
class ReminderForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'reminder_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Настройка заголовков полей
        self.fields['title'].label = 'Текст напоминания'
        self.fields['description'].label = 'Описание'
        self.fields['reminder_time'].label = 'Время напоминания'
        
        # Настройка внешнего вида полей
        self.fields['title'].widget = forms.TextInput(attrs={'placeholder': 'Введите текст'})
        self.fields['description'].widget = forms.Textarea(attrs={'placeholder': 'Введите описание', 'rows': 4})
        self.fields['reminder_time'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        
        # Делаем поле времени обязательным
        self.fields['reminder_time'].required = True