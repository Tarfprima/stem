from django.contrib import admin
# django.urls - модуль маршрутизации Django
# path - создает единичные маршруты
# include - подключает маршруты из других приложений
# Без этого импорта: не работает URL маршрутизация между приложениями
from django.urls import path, include
from django.conf import settings
# django.conf.urls.static.static - функция для обработки статических файлов в режиме разработки
# Создает маршруты для CSS, JS, изображений когда DEBUG=True
# Без этого импорта: не работают статические файлы (стили, скрипты) в режиме разработки
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls), 
    path('', include('stem.urls')), # подключаем URLs из приложения stem Путь для открытия base.html теперь выглядит вот так: "http://127.0.0.1:8000" 

]

# Добавляем обработку статических файлов для разработки
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

