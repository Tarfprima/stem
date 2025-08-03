from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls), 
    path('', include('stem.urls')), # подключаем URLs из приложения stem Путь для открытия base.html теперь выглядит вот так: "http://127.0.0.1:8000" 

]

# Добавляем обработку статических файлов для разработки
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

