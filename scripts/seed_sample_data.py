import os
import django
from decimal import Decimal
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evaluacion2.settings')
django.setup()

from gestion.models import Cliente, Producto, Venta, DetalleVenta

# Datos cotidianos, estilo estudiante
clientes = [
    {'rut': '12.345.678-9', 'nombre': 'Juan Pérez', 'email': 'juan.perez@student.local', 'telefono': '+56 9 1234 5678'},
    {'rut': '98.765.432-1', 'nombre': 'Panadería El Trigal', 'email': 'contacto@eltrigal.local', 'telefono': '+56 2 2345 6789'},
    {'rut': '20.345.678-0', 'nombre': 'Cachureos Tech', 'email': 'ventas@cachureos.local', 'telefono': '+56 2 9876 5432'},
]

productos = [
    {'codigo': 'CUAD-001', 'nombre': 'Cuaderno A4 100 hojas', 'precio': Decimal('1.50'), 'stock': 100},
    {'codigo': 'LAPI-002', 'nombre': 'Lapicero azul', 'precio': Decimal('0.50'), 'stock': 200},
    {'codigo': 'MOCH-003', 'nombre': 'Mochila escolar', 'precio': Decimal('25.00'), 'stock': 20},
    {'codigo': 'CARG-004', 'nombre': 'Cargador USB-C', 'precio': Decimal('12.99'), 'stock': 15},
    {'codigo': 'AUDI-005', 'nombre': 'Audífonos intraaurales', 'precio': Decimal('9.99'), 'stock': 30},
]

print('Creando clientes...')
for c in clientes:
    obj, created = Cliente.objects.get_or_create(rut=c['rut'], defaults={
        'nombre': c['nombre'], 'email': c['email'], 'telefono': c['telefono']
    })
    print('-' if created else '*', obj)

print('\nCreando productos...')
for p in productos:
    obj, created = Producto.objects.get_or_create(codigo=p['codigo'], defaults={
        'nombre': p['nombre'], 'precio': p['precio'], 'stock': p['stock']
    })
    print('-' if created else '*', obj)

# Crear algunas ventas sencillas
print('\nCreando ventas de ejemplo...')
juan = Cliente.objects.filter(rut='12.345.678-9').first()
panaderia = Cliente.objects.filter(rut='98.765.432-1').first()

cuaderno = Producto.objects.get(codigo='CUAD-001')
lapicero = Producto.objects.get(codigo='LAPI-002')
mochila = Producto.objects.get(codigo='MOCH-003')

# Venta 1: Juan compra 2 cuadernos y 3 lapiceros
v1 = Venta.objects.create(cliente=juan, fecha=datetime.now() - timedelta(days=2))
DetalleVenta.objects.create(venta=v1, producto=cuaderno, cantidad=2, precio_unitario=cuaderno.precio)
DetalleVenta.objects.create(venta=v1, producto=lapicero, cantidad=3, precio_unitario=lapicero.precio)
# Actualizar total y stock
v1.total = sum([d.cantidad * d.precio_unitario for d in v1.detalles.all()])
v1.save()
cuaderno.stock = max(0, cuaderno.stock - 2); cuaderno.save()
lapicero.stock = max(0, lapicero.stock - 3); lapicero.save()
print('-', v1, 'Total:', v1.total)

# Venta 2: Panadería compra 5 mochilas (un ejemplo raro pero de prueba)
v2 = Venta.objects.create(cliente=panaderia, fecha=datetime.now() - timedelta(days=1))
DetalleVenta.objects.create(venta=v2, producto=mochila, cantidad=5, precio_unitario=mochila.precio)
v2.total = sum([d.cantidad * d.precio_unitario for d in v2.detalles.all()])
v2.save()
mochila.stock = max(0, mochila.stock - 5); mochila.save()
print('-', v2, 'Total:', v2.total)

print('\nSeed completado.')
