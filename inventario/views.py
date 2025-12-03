from django.shortcuts import render, redirect
from django.http import HttpResponse
from productos.models import Producto

def inicio(request):
    return render(request, "inventario/inicio.html")

def crear_producto(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        nombre = request.POST.get("nombre")
        categoria = request.POST.get("categoria")
        stock = request.POST.get("stock")
        stock_minimo = request.POST.get("stock_minimo")
        stock_maximo = request.POST.get("stock_maximo")
        precio = request.POST.get("precio")


        Producto.objects.create(codigo=codigo , nombre=nombre, categoria = categoria, stock= stock, stock_minimo=stock_minimo, stock_maximo=stock_maximo, precio=precio)
        return redirect("listar_productos")
    
        
    return render(request, "productos/crear.html")

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, "productos/listar.html", {"productos":productos} )
