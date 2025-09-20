# Импортируем необходимые модули
from django.utils import timezone 
from django.shortcuts import render, redirect, get_object_or_404  # render для шаблонов, redirect для перенаправлений, Импортируем функцию для получения объекта или ошибки 404
from django.contrib import messages  # Для сообщений об успехе или ошибке
from django.contrib.auth import authenticate, login, logout  # Для авторизации
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm  # Стандартные формы Django (не используем кастомные, чтобы не усложнять)
from django.contrib.auth.decorators import login_required  # Декоратор для защиты страниц
from .forms import NoteForm, ReminderForm  # Импортируем формы
from .models import Task # Импортируем модель Task для работы с базой данных
from django.views.decorators.http import require_POST # Импортируем декоратор, который разрешает только POST запросы
from django.core.paginator import Paginator
from datetime import timedelta 


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
            return redirect('stem:profile')  # Перенаправляем на профиль
        else:
            messages.error(request, 'Ошибка в форме.')  # Показываем сообщение об ошибке
    else:
        form = ReminderForm()  # Пустая форма для GET-запроса
    # Рендерим шаблон с формой
    return render(request, 'stem/add_reminder.html', {'form': form})

# Функция проверки и маркировки просроченных задач
def check_overdue_tasks(user):
    overdue_time = timezone.now() - timedelta(minutes=2)
    Task.objects.filter(
        user=user, reminder_time__lt=overdue_time, reminder_time__isnull=False,
        completed=False, overdue=False
    ).update(overdue=True)

# Страница профиля
@login_required
def profile(request):
    check_overdue_tasks(request.user)
    
    # Оптимизированные запросы
    user_tasks = Task.objects.filter(user=request.user)
    active_tasks = user_tasks.filter(completed=False, overdue=False).order_by('-created_at')
    
    # Пагинация активных задач
    active_page = Paginator(active_tasks, 12).get_page(request.GET.get('page', 1))

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
    return redirect('stem:login')  # Перенаправляем на напоминания 

@login_required
@require_POST
def delete_task(request, task_id):
    get_object_or_404(Task, id=task_id, user=request.user).delete()
    return redirect('stem:profile')

@login_required
@require_POST
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed, task.overdue = True, False
    task.save()
    return redirect('stem:profile')