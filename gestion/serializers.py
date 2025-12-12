from rest_framework import serializers
from .models import Cliente, Producto, Venta, DetalleVenta
from django.contrib.auth.models import User

# Para mostrar datos básicos del usuario
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# Convierte el modelo Cliente a JSON
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

# Convierte el modelo Producto a JSON
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

# Detalle de venta: incluye nombre del producto y subtotal
class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)  # nombre del producto
    subtotal = serializers.SerializerMethodField()  # subtotal calculado

    class Meta:
        model = DetalleVenta
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'precio_unitario', 'subtotal']

    def get_subtotal(self, obj):
        return obj.cantidad * obj.precio_unitario

# Serializador para ventas: cliente, fecha, total y detalles
class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)  # nombre del cliente
    detalles = DetalleVentaSerializer(many=True, read_only=True)  # lista de detalles
    fecha_formateada = serializers.SerializerMethodField()  # fecha legible

    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'cliente_nombre', 'fecha', 'fecha_formateada', 'total', 'detalles']

    def get_fecha_formateada(self, obj):
        # Formatea la fecha como DD/MM/YYYY
        return obj.fecha.strftime('%d/%m/%Y %H:%M') if obj.fecha else ""

class DashboardSerializer(serializers.Serializer):
    total_clientes = serializers.IntegerField()
    total_productos = serializers.IntegerField()
    total_ventas = serializers.IntegerField()
    ventas_mes_actual = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    productos_mas_vendidos = ProductoSerializer(many=True)
    clientes_top = ClienteSerializer(many=True)

class ProductoVentaSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField()
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

class VentaCreateSerializer(serializers.Serializer):
    cliente_id = serializers.IntegerField()
    productos = ProductoVentaSerializer(many=True)