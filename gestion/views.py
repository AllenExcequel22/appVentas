from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Producto, Venta, DetalleVenta
from django.db.models import Sum, Count
from .forms import ClienteForm, ProductoForm

def home(request):
    # Productos más vendidos (ordenados por cantidad total vendida)
    productos_mas_vendidos = Producto.objects.annotate(
        total_vendido=Sum('detalleventa__cantidad')
    ).order_by('-total_vendido')[:5]
    
    # Clientes con más ventas (ordenados por número de ventas)
    clientes_top = Cliente.objects.annotate(
        total_ventas=Count('venta')
    ).order_by('-total_ventas')[:5]
    
    return render(request, 'home.html', {
        'productos_mas_vendidos': productos_mas_vendidos,
        'clientes_top': clientes_top
    })

# Vistas para Clientes
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/list.html', {'clientes': clientes})

def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'clientes/form.html', {'form': form, 'titulo': 'Crear Cliente'})

def cliente_edit(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/form.html', {'form': form, 'titulo': 'Editar Cliente'})

def cliente_delete(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_list')
    return render(request, 'clientes/delete.html', {'cliente': cliente})

# Vistas para Productos
def producto_list(request):
    productos = Producto.objects.all()
    return render(request, 'productos/list.html', {'productos': productos})

def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('producto_list')
    else:
        form = ProductoForm()
    return render(request, 'productos/form.html', {'form': form, 'titulo': 'Crear Producto'})

def producto_edit(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('producto_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/form.html', {'form': form, 'titulo': 'Editar Producto'})

def producto_delete(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('producto_list')
    return render(request, 'productos/delete.html', {'producto': producto})

from django.forms import inlineformset_factory

# Crear el formset para detalles de venta
DetalleVentaFormSet = inlineformset_factory(
    Venta, DetalleVenta, 
    fields=('producto', 'cantidad', 'precio_unitario'), 
    extra=1,
    can_delete=True
)

# Vistas para Ventas
def venta_list(request):
    ventas = Venta.objects.all().select_related('cliente')
    return render(request, 'ventas/list.html', {'ventas': ventas})

def venta_create(request):
    if request.method == 'POST':
        # Lógica para crear venta (la haremos simple por ahora)
        cliente_id = request.POST.get('cliente')
        cliente = get_object_or_404(Cliente, id=cliente_id)
        venta = Venta.objects.create(cliente=cliente, total=0)
        return redirect('venta_list')
    else:
        clientes = Cliente.objects.all()
        productos = Producto.objects.all()
        return render(request, 'ventas/form.html', {
            'clientes': clientes,
            'productos': productos,
            'titulo': 'Crear Venta'
        })

def venta_detail(request, id):
    venta = get_object_or_404(Venta, id=id)
    detalles = venta.detalles.all().select_related('producto')
    return render(request, 'ventas/detail.html', {
        'venta': venta,
        'detalles': detalles
    })

def venta_delete(request, id):
    venta = get_object_or_404(Venta, id=id)
    if request.method == 'POST':
        venta.delete()
        return redirect('venta_list')
    return render(request, 'ventas/delete.html', {'venta': venta})