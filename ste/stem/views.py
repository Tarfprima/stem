from django.shortcuts import render, redirect
from . import models # Чтобы обратиться к базе данных используем "модели" что-бы обратиться к моделям из них надо испортировать наш код. 

# Функция для отображения base.html 
def index(request):
    return render(request, 'stem/index.html')

def add_task(request):
    return render(request, 'stem/add_task.html')

def profile(request):
    return render(request, 'stem/profile.html')

def login_view(request):
    return render(request, 'stem/login.html')

def register_view(request):
    return render(request, 'stem/register.html')