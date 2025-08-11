from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

# Главная страница
def index(request):
    # Рендерит шаблон главной страницы
    return render(request, 'stem/index.html')

# Страница профиля, защищена декоратором login_required
@login_required
def profile(request):
    # Рендерит шаблон профиля
    return render(request, 'stem/profile.html')

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
                messages.success(request, 'Вы успешно вошли!')
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
                messages.success(request, 'Регистрация успешна!')
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
    messages.success(request, 'Вы успешно вышли!')
    return redirect('stem:index')  # Перенаправляем на главную