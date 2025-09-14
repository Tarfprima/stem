# stem/urls.py

# Импортируем path для создания маршрутов (стандартный импорт в Django)
from django.urls import path
# Импортируем представления из текущей папки
from . import views

# Пространство имён для URL, чтобы избежать конфликтов (актуальный подход в Django)
app_name = 'stem' # app_name = 'stem' — пространство имён для URL, чтобы использовать {% url 'stem:add_note' %} в шаблонах
urlpatterns = [
    # Страница добавления заметки
    path('', views.add_note, name='add_note'),
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