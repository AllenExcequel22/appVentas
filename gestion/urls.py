from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('', views.home, name='home'),
]

# Ventas
path('ventas/', views.venta_list, name='venta_list'),
path('ventas/crear/', views.venta_create, name='venta_create'),
path('ventas/<int:id>/', views.venta_detail, name='venta_detail'),
path('ventas/eliminar/<int:id>/', views.venta_delete, name='venta_delete'),