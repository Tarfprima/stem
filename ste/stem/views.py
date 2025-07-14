from django.shortcuts import render, redirect
from . import models # Чтобы обратиться к базе данных используем "модели" что-бы обратиться к моделям из них надо испортировать наш код. 

# Функция для отображения base.html 
def index(request):
    return render(request, 'stem/index.html')