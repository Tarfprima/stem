# django.forms - модуль Django для создания HTML форм и их валидации
# Предоставляет классы Form, ModelForm, CharField, TextInput и другие виджеты
# Без этого импорта: невозможно создавать веб-формы, нет валидации пользовательского ввода
from django import forms

# Импорт нашей модели Task из текущего приложения
# Используется для создания ModelForm - форм, автоматически связанных с моделью
# Без этого импорта: нельзя создавать формы для создания/редактирования задач
from .models import Task

# Форма для добавления заметки (без времени)
class NoteForm(forms.ModelForm):  # NoteForm - класс формы наследуется от ModelForm
    class Meta:  # Meta - внутренний класс с настройками формы
        # Связываем форму с моделью Task
        model = Task  # указание модели для автогенерации полей
        # Указываем поля формы (title и description)
        fields = ['title', 'description']  # список полей для отображения в форме
        # Лейблы для полей (на русском)
        labels = {  # словарь подписей полей
            'title': 'Название заметки',
            'description': 'Описание',
        }
        # Виджеты для стилизации 
        widgets = {  # словарь виджетов HTML для полей
            'title': forms.TextInput(attrs={'placeholder': 'Введите название'}),  # TextInput - виджет текстового поля
            'description': forms.Textarea(attrs={'placeholder': 'Введите описание', 'rows': 4}),  # Textarea - виджет многострочного текста
        }

# Форма для добавления напоминания (с обязательным временем)
class ReminderForm(forms.ModelForm):  # ReminderForm - класс формы для напоминаний
    class Meta:
        model = Task  # связь с моделью Task
        fields = ['title', 'description', 'reminder_time']  # поля включая reminder_time
        labels = {
            'title': 'Текст напоминания',
            'description': 'Описание',
            'reminder_time': 'Время напоминания',  # подпись для поля времени
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите текст'}),
            'description': forms.Textarea(attrs={'placeholder': 'Введите описание', 'rows': 4}),
            'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # DateTimeInput - виджет выбора даты и времени; 'type': 'datetime-local' - HTML5 элемент выбора времени
        }

    # Переопределяем init для обязательного поля reminder_time
    def __init__(self, *args, **kwargs):  # __init__ - метод инициализации класса; *args, **kwargs - переменное количество аргументов
        super().__init__(*args, **kwargs)  # вызов инициализации родительского класса
        self.fields['reminder_time'].required = True  # required = True - делает поле обязательным для заполнения
        
# forms.ModelForm — способ создания форм в Django, связанный с моделью (автоматически создаёт поля).
# fields — указывает, какие поля модели использовать в форме.
# labels — меняет названия полей на русский (для читаемости).
# widgets — добавляет атрибуты для стилизации (placeholder для подсказок, rows для высоты textarea).
# __init__ — магический метод, который инициализирует форму и делает reminder_time обязательным (required=True).
# Для заметок (NoteForm) — без reminder_time, для напоминаний (ReminderForm) — с обязательным полем времени.