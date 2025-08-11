from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # Вход/регистрация: Использую встроенные формы AuthenticationForm и UserCreationForm.
from django.contrib import messages
from .forms import TaskForm # Форма TaskForm сохраняет задачи, привязанные к пользователю.
from .models import Task

def index(request):
    return render(request, 'stem/index.html')

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Задача успешно добавлена!')
            return redirect('stem:profile')
    else:
        form = TaskForm()
    return render(request, 'stem/add_task.html', {'form': form})

# Профиль: Отображаем реальные задачи из базы, с разделением на активные и завершённые.
@login_required
def profile(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    active_tasks = tasks.filter(completed=False)
    completed_tasks = tasks.filter(completed=True)
    return render(request, 'stem/profile.html', {
        'active_tasks': active_tasks,
        'completed_tasks': completed_tasks,
        'total_tasks': tasks.count(),
        'active_count': active_tasks.count(),
        'completed_count': completed_tasks.count(),
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли!')
                return redirect('stem:profile')
            else:
                messages.error(request, 'Неверный логин или пароль.')
        else:
            messages.error(request, 'Ошибка в форме.')
    else:
        form = AuthenticationForm()
    return render(request, 'stem/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('stem:profile')
        else:
            messages.error(request, 'Ошибка в форме регистрации.')
    else:
        form = UserCreationForm()
    return render(request, 'stem/register.html', {'form': form})

def about(request):
    return render(request, 'stem/about.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли!')
    return redirect('stem:index')