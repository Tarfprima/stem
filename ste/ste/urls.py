from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls), 
    path('', include('stem.urls')), # Путь для открытия stem_main.html теперь выглядит вот так: "http://127.0.0.1:8000/stem/" 

]

