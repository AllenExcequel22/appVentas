from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Cliente, Producto, Venta, DetalleVenta
from django.db.models import Sum, Count
from .forms import ClienteForm, ProductoForm
from django.forms import inlineformset_factory

# VISTA DE REGISTRO
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'auth/registro.html', {'form': form})

# VISTAS PROTEGIDAS
@login_required
def home(request):
    productos_mas_vendidos = Producto.objects.annotate(
        total_vendido=Sum('detalleventa__cantidad')
    ).order_by('-total_vendido')[:5]
    
    clientes_top = Cliente.objects.annotate(
        total_ventas=Count('venta')
    ).order_by('-total_ventas')[:5]
    
    return render(request, 'gestion/home.html', {
        'productos_mas_vendidos': productos_mas_vendidos,
        'clientes_top': clientes_top
    })

# CLIENTES
@login_required
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/list.html', {'clientes': clientes})

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'clientes/form.html', {'form': form, 'titulo': 'Crear Cliente'})

@login_required
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

@login_required
def cliente_delete(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_list')
    return render(request, 'clientes/delete.html', {'cliente': cliente})

# PRODUCTOS
@login_required
def producto_list(request):
    productos = Producto.objects.all()
    return render(request, 'productos/list.html', {'productos': productos})

@login_required
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('producto_list')
    else:
        form = ProductoForm()
    return render(request, 'productos/form.html', {'form': form, 'titulo': 'Crear Producto'})

@login_required
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

@login_required
def producto_delete(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('producto_list')
    return render(request, 'productos/delete.html', {'producto': producto})

# VENTAS
DetalleVentaFormSet = inlineformset_factory(
    Venta, DetalleVenta, 
    fields=('producto', 'cantidad', 'precio_unitario'), 
    extra=1,
    can_delete=True
)

@login_required
def venta_list(request):
    ventas = Venta.objects.all().select_related('cliente')
    return render(request, 'ventas/list.html', {'ventas': ventas})

@login_required
def venta_create(request):
    if request.method == 'POST':
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

@login_required
def venta_detail(request, id):
    venta = get_object_or_404(Venta, id=id)
    detalles = venta.detalles.all().select_related('producto')
    return render(request, 'ventas/detail.html', {
        'venta': venta,
        'detalles': detalles
    })

@login_required
def venta_delete(request, id):
    venta = get_object_or_404(Venta, id=id)
    if request.method == 'POST':
        venta.delete()
        return redirect('venta_list')
    return render(request, 'ventas/delete.html', {'venta': venta})