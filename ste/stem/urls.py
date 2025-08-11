from django.urls import path
from . import views

# Пространство имён для URL, чтобы избежать конфликтов
app_name = 'stem'
urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
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