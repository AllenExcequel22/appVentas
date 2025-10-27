from django.contrib import admin
from django.urls import path, include  # Asegúrate de incluir 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion.urls')),  # Incluye las URLs de tu app
]