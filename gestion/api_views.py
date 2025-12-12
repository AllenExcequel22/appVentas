from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count, Q
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Cliente, Producto, Venta, DetalleVenta
from .serializers import (
    ClienteSerializer, 
    ProductoSerializer, 
    VentaSerializer, 
    DashboardSerializer,
    UserSerializer,
    VentaCreateSerializer,
    DetalleVentaSerializer
)

# Registra usuarios desde la API
class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Crea usuario si el nombre no existe
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'El nombre de usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)

        return Response({'message': 'Usuario registrado exitosamente', 'user_id': user.id}, status=status.HTTP_201_CREATED)

# Devuelve datos del usuario autenticado
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# Clientes: listar/crear/editar/eliminar
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Buscar clientes por nombre o rut
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        nombre = request.query_params.get('nombre', '')
        rut = request.query_params.get('rut', '')

        queryset = self.queryset
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if rut:
            queryset = queryset.filter(rut__icontains=rut)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Productos: listar/crear/editar/eliminar
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Productos con stock bajo
    @action(detail=False, methods=['get'])
    def baja_stock(self, request):
        productos = Producto.objects.filter(stock__lt=10).order_by('stock')
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    # Productos más vendidos
    @action(detail=False, methods=['get'])
    def mas_vendidos(self, request):
        productos = Producto.objects.annotate(total_vendido=Sum('detalleventa__cantidad')).order_by('-total_vendido')[:10]
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    # Productos disponibles (stock > 0)
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        productos = Producto.objects.filter(stock__gt=0)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

# Ventas: listar, crear y ver detalles
class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all().select_related('cliente').order_by('-fecha')
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Crear una venta con varios productos
    def create(self, request):
        serializer = VentaCreateSerializer(data=request.data)
        if serializer.is_valid():
            cliente_id = serializer.validated_data['cliente_id']
            productos_data = serializer.validated_data['productos']

            cliente = get_object_or_404(Cliente, id=cliente_id)
            venta = Venta.objects.create(cliente=cliente, total=0)

            total_venta = 0
            detalles = []

            for item in productos_data:
                producto = get_object_or_404(Producto, id=item['producto_id'])
                cantidad = item['cantidad']
                precio = item.get('precio_unitario', producto.precio)

                if producto.stock < cantidad:
                    venta.delete()
                    return Response({'error': f'Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}'}, status=status.HTTP_400_BAD_REQUEST)

                detalle = DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio
                )
                detalles.append(detalle)

                total_venta += cantidad * precio
                producto.stock -= cantidad
                producto.save()

            venta.total = total_venta
            venta.save()

            venta_serializer = VentaSerializer(venta)
            return Response(venta_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Obtener detalles de una venta
    @action(detail=True, methods=['get'])
    def detalles(self, request, pk=None):
        venta = self.get_object()
        detalles = venta.detalles.all().select_related('producto')
        serializer = DetalleVentaSerializer(detalles, many=True)
        return Response(serializer.data)

    # Filtrar ventas por rango de fechas
    @action(detail=False, methods=['get'])
    def por_fecha(self, request):
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        queryset = self.queryset

        if fecha_inicio and fecha_fin:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)
                queryset = queryset.filter(fecha__range=[fecha_inicio, fecha_fin])
            except ValueError:
                return Response({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Si no se pasan fechas, muestra las ventas de los últimos 30 días
            fecha_fin = timezone.now()
            fecha_inicio = fecha_fin - timedelta(days=30)
            queryset = queryset.filter(fecha__range=[fecha_inicio, fecha_fin])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Ventas de un cliente específico
    @action(detail=False, methods=['get'])
    def por_cliente(self, request):
        cliente_id = request.query_params.get('cliente_id')
        if cliente_id:
            queryset = self.queryset.filter(cliente_id=cliente_id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'error': 'Se requiere cliente_id'}, status=status.HTTP_400_BAD_REQUEST)

# Datos resumidos para el dashboard
class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Calcula totales y rankings simples
        total_clientes = Cliente.objects.count()
        total_productos = Producto.objects.count()
        total_ventas = Venta.objects.count()

        hoy = timezone.now()
        inicio_mes = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        ventas_mes = Venta.objects.filter(fecha__gte=inicio_mes)
        ventas_mes_actual = ventas_mes.aggregate(total=Sum('total'))['total'] or 0

        productos_mas_vendidos = Producto.objects.annotate(total_vendido=Sum('detalleventa__cantidad')).order_by('-total_vendido')[:5]
        clientes_top = Cliente.objects.annotate(total_ventas=Count('venta'), monto_total=Sum('venta__total')).order_by('-total_ventas')[:5]

        data = {
            'total_clientes': total_clientes,
            'total_productos': total_productos,
            'total_ventas': total_ventas,
            'ventas_mes_actual': ventas_mes_actual,
            'productos_mas_vendidos': ProductoSerializer(productos_mas_vendidos, many=True).data,
            'clientes_top': ClienteSerializer(clientes_top, many=True).data,
        }

        serializer = DashboardSerializer(data)
        return Response(serializer.data)