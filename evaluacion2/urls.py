from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from gestion import views

urlpatterns = [
    # 🔧 Panel de administración Django
    path('admin/', admin.site.urls),
    
    # 🔐 Autenticación web (HTML templates)
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', views.registro, name='registro'),
    
    # 🌐 API RESTful (v1)
    path('api/v1/', include('gestion.api_urls')),
    
    # 🖥️ Aplicación web principal
    path('', include('gestion.urls')),
]