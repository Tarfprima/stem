# Импортируем необходимые модули
from django.shortcuts import render, redirect  # render для шаблонов, redirect для перенаправлений
from django.contrib import messages  # Для сообщений об успехе или ошибке
from django.contrib.auth import authenticate, login, logout  # Для авторизации
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm  # Стандартные формы Django (не используем кастомные, чтобы не усложнять)
from django.contrib.auth.decorators import login_required  # Декоратор для защиты страниц
from .forms import NoteForm, ReminderForm  # Импортируем формы
from .models import Task # Импортируем модель Task для работы с базой данных

# Страница добавления заметки
@login_required
def add_note(request):
    # Если пользователь отправил форму (POST)
    if request.method == 'POST':
        form = NoteForm(request.POST)  # Создаём форму с данными из запроса
        if form.is_valid():
            task = form.save(commit=False)  # Создаём объект задачи, но не сохраняем сразу
            task.user = request.user  # Привязываем задачу к текущему пользователю
            task.save()  # Сохраняем задачу в базе
            messages.success(request, 'Заметка добавлена!')  # Показываем сообщение об успехе
            return redirect('stem:profile')  # Перенаправляем на профиль
        else:
            messages.error(request, 'Ошибка в форме.')  # Показываем сообщение об ошибке
    else:
        form = NoteForm()  # Пустая форма для GET-запроса
    # Рендерим шаблон с формой
    return render(request, 'stem/add_note.html', {'form': form})

# Страница добавления напоминания
@login_required
def add_reminder(request):
    # Если пользователь отправил форму (POST)
    if request.method == 'POST':
        form = ReminderForm(request.POST)  # Создаём форму с данными из запроса
        if form.is_valid():
            task = form.save(commit=False)  # Создаём объект задачи, но не сохраняем сразу
            task.user = request.user  # Привязываем задачу к текущему пользователю
            task.save()  # Сохраняем задачу в базе
            messages.success(request, 'Напоминание добавлено!')  # Показываем сообщение об успехе
            return redirect('stem:profile')  # Перенаправляем на профиль
        else:
            messages.error(request, 'Ошибка в форме.')  # Показываем сообщение об ошибке
    else:
        form = ReminderForm()  # Пустая форма для GET-запроса
    # Рендерим шаблон с формой
    return render(request, 'stem/add_reminder.html', {'form': form})

# Страница профиля
@login_required
def profile(request):
    # Получаем задачи текущего пользователя, сортируем по дате создания (новые сверху)
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    # Разделяем задачи на активные и завершённые
    active_tasks = tasks.filter(completed=False)
    completed_tasks = tasks.filter(completed=True)
    # Передаём задачи и статистику в шаблон
    return render(request, 'stem/profile.html', {
        'active_tasks': active_tasks,
        'completed_tasks': completed_tasks,
        'total_tasks': tasks.count(),
        'active_count': active_tasks.count(),
        'completed_count': completed_tasks.count(),
    })

# Страница входа
def login_view(request):
    # Если пользователь отправил форму (POST)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('stem:profile')  # Перенаправляем на профиль
            else:
                messages.error(request, 'Неверный логин или пароль.')
        else:
            messages.error(request, 'Ошибка в форме.')
    else:
        form = AuthenticationForm()
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
    return redirect('stem:add_reminder')  # Перенаправляем на напоминания 