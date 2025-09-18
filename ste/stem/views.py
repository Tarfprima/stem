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
from django.utils import timezone 


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

# Страница профиля
@login_required
def profile(request):
    # Все активные задачи (completed=False), новые сверху
    active_tasks = Task.objects.filter(user=request.user, completed=False).order_by('-created_at')
    # Пагинация только активных задач
    paginator = Paginator(active_tasks, 10)
    page_number = request.GET.get('page', 1)
    active_page = paginator.get_page(page_number)

    # Все завершённые задачи (completed=True), новые сверху
    completed_tasks = Task.objects.filter(user=request.user, completed=True).order_by('-created_at')

    return render(request, 'stem/profile.html', {
        'active_page': active_page,
        'completed_tasks': completed_tasks,
        'total_tasks': Task.objects.filter(user=request.user).count(),
        'active_count': active_tasks.count(),
        'completed_count': completed_tasks.count(),
        'now': timezone.now(),
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

@login_required  # Декоратор - функция доступна только авторизованным пользователям
@require_POST    # Декоратор - функция принимает только POST запросы (безопасность)
def delete_task(request, task_id):
    # request - объект запроса от пользователя
    # task_id - ID задачи из URL (например, /delete/5/ -> task_id = 5)
    
    # Ищем задачу по ID и проверяем, что она принадлежит текущему пользователю
    # Если задача не найдена или не принадлежит пользователю - вернет ошибку 404
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    # Удаляем задачу из базы данных
    task.delete()
    
    # Перенаправляем пользователя обратно на страницу профиля
    return redirect('stem:profile')

@login_required                  # Доступ только для авторизованных
@require_POST                    # Разрешаем только POST-запросы
def complete_task(request, task_id):
    # Ищем задачу по ID и пользователю, 404 если не найдена
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    # Помечаем задачу как завершённую
    task.completed = True
    task.save()                 # Сохраняем изменение в базе
        
    # Возвращаемся на профиль
    return redirect('stem:profile')