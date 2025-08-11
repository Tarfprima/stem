# Это urls.py для приложения, а есть urls.py глобальный, который находится в файле ste, необходимо чтобы путь из глобального urls.py ввель в путь urls.py из приложения.
from django.urls import path
from . import views # Импорт содержимого файла views.py т.е получения доступа к содержимому файла.


app_name = 'stem' # переменная с строкой stem для будущего использования 
urlpatterns = [
    # Путь к страницам
    path('', views.index, name='index'), # Ссылка на главную страницу: http://127.0.0.1:8000
    path('add/', views.add_task, name='add_task'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),
]