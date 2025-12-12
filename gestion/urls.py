from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    # Dashboard - ESTA ES LA URL 'home'
    path('', views.home, name='home'),  # ← ¡ESTA LÍNEA DEBE EXISTIR!
    
    # Clientes
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/crear/', views.cliente_create, name='cliente_create'),
    path('clientes/editar/<int:id>/', views.cliente_edit, name='cliente_edit'),
    path('clientes/eliminar/<int:id>/', views.cliente_delete, name='cliente_delete'),
    
    # Productos
    path('productos/', views.producto_list, name='producto_list'),
    path('productos/crear/', views.producto_create, name='producto_create'),
    path('productos/editar/<int:id>/', views.producto_edit, name='producto_edit'),
    path('productos/eliminar/<int:id>/', views.producto_delete, name='producto_delete'),
    
    # Ventas
    path('ventas/', views.venta_list, name='venta_list'),
    path('ventas/crear/', views.venta_create, name='venta_create'),
    path('ventas/<int:id>/', views.venta_detail, name='venta_detail'),
    path('ventas/eliminar/<int:id>/', views.venta_delete, name='venta_delete'),
]