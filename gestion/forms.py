from django import forms
from .models import Cliente, Producto

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rut', 'nombre', 'email', 'telefono']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'nombre': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'telefono': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'precio', 'stock']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'nombre': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'precio': forms.NumberInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
        }