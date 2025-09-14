# Импортируем модуль forms для создания форм
from django import forms
# Импортируем модель Task для связи с базой данных
from .models import Task

# Форма для добавления заметки (без времени)
class NoteForm(forms.ModelForm):
    class Meta:
        # Связываем форму с моделью Task
        model = Task
        # Указываем поля формы (title и description)
        fields = ['title', 'description']
        # Лейблы для полей (на русском)
        labels = {
            'title': 'Название заметки',
            'description': 'Описание',
        }
        # Виджеты для стилизации 
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите название'}),
            'description': forms.Textarea(attrs={'placeholder': 'Введите описание', 'rows': 4}),
        }

# Форма для добавления напоминания (с обязательным временем)
class ReminderForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'reminder_time']
        labels = {
            'title': 'Текст напоминания',
            'description': 'Описание',
            'reminder_time': 'Время напоминания',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите текст'}),
            'description': forms.Textarea(attrs={'placeholder': 'Введите описание', 'rows': 4}),
            'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Современный виджет для выбора времени
        }

    # Переопределяем init для обязательного поля reminder_time
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reminder_time'].required = True  # Делаем поле обязательным
        
# forms.ModelForm — способ создания форм в Django, связанный с моделью (автоматически создаёт поля).
# fields — указывает, какие поля модели использовать в форме.
# labels — меняет названия полей на русский (для читаемости).
# widgets — добавляет атрибуты для стилизации (placeholder для подсказок, rows для высоты textarea).
# __init__ — магический метод, который инициализирует форму и делает reminder_time обязательным (required=True).
# Для заметок (NoteForm) — без reminder_time, для напоминаний (ReminderForm) — с обязательным полем времени.