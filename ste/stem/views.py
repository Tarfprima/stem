# django.utils.timezone - модуль для работы с временными зонами в Django
from django.utils import timezone
# render - рендерит HTML шаблоны с контекстом
# redirect - перенаправляет на другие URL
# get_object_or_404 - получает объект из БД или возвращает 404 ошибку
from django.shortcuts import render, redirect, get_object_or_404
# django.contrib.messages - система сообщений Django для пользователей
# Позволяет показывать уведомления об успехе/ошибках между HTTP запросами
from django.contrib import messages
# django.contrib.auth - модуль аутентификации Django
from django.contrib.auth import authenticate, login, logout
# django.contrib.auth.forms - встроенные формы Django для авторизации
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# django.contrib.auth.decorators.login_required - декоратор защиты view-функций
# Автоматически перенаправляет неавторизованных пользователей на страницу входа
# Без этого: незащищенные страницы доступны всем пользователям
from django.contrib.auth.decorators import login_required
# Импорт наших кастомных форм из текущего приложения
# NoteForm - форма создания заметок без времени
# ReminderForm - форма создания напоминаний с временем
from .forms import NoteForm, ReminderForm
# TelegramProfile - модель связи пользователей с Telegram
from .models import Task, TelegramProfile
# django.views.decorators.http.require_POST - декоратор ограничения HTTP методов
# Разрешает доступ к view только через POST запросы
# Без этого: небезопасные операции могут выполняться через GET запросы
from django.views.decorators.http import require_POST
# django.core.paginator.Paginator - класс для разбивки данных на страницы
# Позволяет отображать большие списки задач частями
from django.core.paginator import Paginator
# datetime.timedelta - класс для работы с временными интервалами
# Используется для определения просроченных задач (сравнение с текущим временем)
# Без этого импорта: не работает логика определения просроченных напоминаний  
from datetime import timedelta 


# Страница добавления заметки
@login_required  # декоратор требующий авторизации пользователя
def add_note(request):  # view-функция для добавления заметки
    # Если пользователь отправил форму (POST)
    if request.method == 'POST':  # проверка HTTP метода запроса
        form = NoteForm(request.POST)  # NoteForm - класс формы для заметок; request.POST - данные из формы
        if form.is_valid():  # is_valid() - метод валидации формы
            task = form.save(commit=False)  # save(commit=False) - создание объекта без сохранения в БД
            task.user = request.user  # request.user - объект текущего пользователя
            task.save()  # сохранение задачи в базу данных
            return redirect('stem:profile')  # redirect() - функция перенаправления на другую страницу
        else:
            messages.error(request, 'Ошибка в форме.')  # messages.error() - функция показа сообщения об ошибке
    else:
        form = NoteForm()  # создание пустой формы для GET-запроса
    # Рендерим шаблон с формой
    return render(request, 'stem/add_note.html', {'form': form})  # render() - функция рендеринга HTML шаблона

# Страница добавления напоминания
@login_required
def add_reminder(request):  # view-функция для добавления напоминания
    # Если пользователь отправил форму (POST)
    if request.method == 'POST':
        form = ReminderForm(request.POST)  # ReminderForm - класс формы для напоминаний с обязательным временем
        if form.is_valid():
            task = form.save(commit=False)  # создание объекта задачи без сохранения
            task.user = request.user  # привязка к текущему пользователю
            task.save()  # сохранение в базу данных
            return redirect('stem:profile')  # перенаправление на страницу профиля
        else:
            messages.error(request, 'Ошибка в форме.')  # показ ошибки валидации
    else:
        form = ReminderForm()  # пустая форма для отображения
    # Рендерим шаблон с формой
    return render(request, 'stem/add_reminder.html', {'form': form})

# Функция проверки и маркировки просроченных задач
def check_overdue_tasks(user):  # функция проверки просроченных задач
    overdue_time = timezone.now() - timedelta(minutes=2)  # timedelta - класс временного интервала; minutes=2 - интервал в 2 минуты
    Task.objects.filter(  # фильтрация задач по условиям
        user=user, reminder_time__lt=overdue_time, reminder_time__isnull=False,  # reminder_time__lt - фильтр "меньше чем"; reminder_time__isnull=False - исключаем задачи без времени
        completed=False, overdue=False
    ).update(overdue=True)  # update() - метод массового обновления записей в БД

# Страница профиля
@login_required
def profile(request):  # view-функция страницы профиля пользователя
    check_overdue_tasks(request.user)  # проверка и обновление просроченных задач
    
    # Создаём Telegram профиль если его нет
    TelegramProfile.objects.get_or_create(user=request.user)  # get_or_create() - метод получения или создания объекта
    
    # Оптимизированные запросы
    user_tasks = Task.objects.filter(user=request.user)  # получение всех задач пользователя
    active_tasks = user_tasks.filter(completed=False, overdue=False).order_by('-created_at')  # фильтрация активных задач; order_by() - сортировка по дате создания
    
    # Пагинация активных задач
    active_page = Paginator(active_tasks, 12).get_page(request.GET.get('page', 1))  # Paginator - класс разбивки на страницы; get_page() - получение конкретной страницы

    return render(request, 'stem/profile.html', {
        'active_page': active_page,
        'completed_tasks': user_tasks.filter(completed=True).order_by('-created_at'),
        'overdue_tasks': user_tasks.filter(overdue=True, completed=False).order_by('-created_at'),
        'active_count': active_tasks.count(),
        'completed_count': user_tasks.filter(completed=True).count(),
        'overdue_count': user_tasks.filter(overdue=True, completed=False).count(),
        'total_tasks': user_tasks.count(),
    })

# Страница входа
def login_view(request):  # view-функция страницы входа
    # Если пользователь отправил форму (POST)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # AuthenticationForm - встроенная форма авторизации Django
        if form.is_valid():
            username = form.cleaned_data.get('username')  # cleaned_data - словарь валидированных данных формы; get() - безопасное получение значения
            password = form.cleaned_data.get('password')  # получение пароля из формы
            user = authenticate(username=username, password=password)  # authenticate() - функция проверки логина и пароля
            if user is not None:  # проверка успешной авторизации
                login(request, user)  # login() - функция входа пользователя в систему
                return redirect('stem:profile')  # перенаправление на профиль
            else:
                messages.error(request, 'Неверный логин или пароль.')  # сообщение об ошибке авторизации
        else:
            messages.error(request, 'Ошибка в форме.')
    else:
        form = AuthenticationForm()  # создание пустой формы авторизации
    # Рендерим шаблон входа с формой
    return render(request, 'stem/login.html', {'form': form})

# Страница регистрации
def register_view(request):
    # Если пользователь отправил форму (POST)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем нового пользователя
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('stem:profile')  # Перенаправляем на профиль
            else:
                messages.error(request, 'Ошибка в форме регистрации.')
        else:
            messages.error(request, 'Ошибка в форме регистрации.')
    else:
        form = UserCreationForm()
    # Рендерим шаблон регистрации с формой
    return render(request, 'stem/register.html', {'form': form})

# Страница "О сайте"
def about(request):
    # Рендерит шаблон "О сайте"
    return render(request, 'stem/about.html')

# Страница выхода
@login_required
def logout_view(request):
    # Выполняет выход пользователя
    logout(request)
    return redirect('stem:login')  # Перенаправляем на напоминания 

@login_required
@require_POST  # декоратор разрешающий только POST запросы
def delete_task(request, task_id):  # view-функция удаления задачи; task_id - параметр ID задачи из URL
    get_object_or_404(Task, id=task_id, user=request.user).delete()  # get_object_or_404() - функция получения объекта или ошибки 404; delete() - метод удаления объекта
    return redirect('stem:profile')  # перенаправление обратно на профиль

@login_required
@require_POST
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed, task.overdue = True, False
    task.save()
    return redirect('stem:profile')

# Функция для отключения Telegram бота от профиля пользователя
@login_required
@require_POST
def disconnect_telegram(request):
    """Отвязывает Telegram бота от профиля пользователя через веб-интерфейс"""
    try:
        # Получаем или создаем Telegram профиль пользователя
        profile, created = TelegramProfile.objects.get_or_create(user=request.user)
        if profile.telegram_chat_id:
            # Если бот был подключен - отключаем его
            profile.telegram_chat_id = None
            profile.save()
            messages.success(request, 'Telegram бот успешно отключен от вашего профиля.')
        else:
            # Если бот уже не подключен
            messages.info(request, 'Telegram бот уже не подключен к вашему профилю.')
    except Exception as e:
        # В случае ошибки
        messages.error(request, 'Произошла ошибка при отключении бота.')
    
    return redirect('stem:profile')