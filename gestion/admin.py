from django.contrib import admin
from .models import Cliente, Producto, Venta, DetalleVenta

# Registrar los modelos para que aparezcan en el admin
admin.site.register(Cliente)
admin.site.register(Producto) 
admin.site.register(Venta)
admin.site.register(DetalleVenta)