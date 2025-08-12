from django.urls import path
from . import views

app_name = 'stem'
urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    # Страница добавления заметки 
    path('add-note/', views.add_note, name='add_note'),
    # Страница добавления напоминания
    path('add-reminder/', views.add_reminder, name='add_reminder'),
    # Страница профиля
    path('profile/', views.profile, name='profile'),
    # Страница входа
    path('login/', views.login_view, name='login'),
    # Страница регистрации
    path('register/', views.register_view, name='register'),
    # Страница "О сайте"
    path('about/', views.about, name='about'),
    # Страница выхода
    path('logout/', views.logout_view, name='logout'),
]