from django.shortcuts import render, redirect
from . import models # Чтобы обратиться к базе данных используем "модели" что-бы обратиться к моделям из них надо испортировать наш код. 

# Функция для отображения stem_main.html 
def stem_main(request): # Функция для рендера главной страницы stem_main.html
    return render(
        request,
        'stem/stem_main.html'
    )

