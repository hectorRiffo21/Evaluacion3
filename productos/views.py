from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Producto
from decimal import Decimal
def crear_producto(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        nombre = request.POST.get("nombre")
        categoria = request.POST.get("categoria")
        stock = request.POST.get("stock")
        stock_minimo = request.POST.get("stock_minimo")
        stock_maximo = request.POST.get("stock_maximo")
        precio = Decimal(request.POST.get("precio"))
        activo = request.POST.get("activo") == "on"

        if Producto.objects.filter(codigo=codigo).exists():
            return HttpResponse("Error: Ya existe un producto con ese codigo")
        if not codigo or not nombre or not stock or not precio:
            messages.error(request, "Faltan campos obligatorios.")
            return render(request, "productos/crear.html")
        

        try:
            stock = int(stock)
            stock_minimo = int(stock_minimo) if stock_minimo else 0
            stock_maximo = int(stock_maximo) if stock_maximo else 99999
            precio = float(precio)
        except ValueError:
            messages.error(request, "Stock y precio deben ser valores numericos.")
            return render(request, "productos/crear.html")
        
        if stock < 0 or precio <=0:
            messages.error(request, "Stock debe ser >=0 y precio > 0.")
            return render(request, "productos/crear.html")
        if stock_minimo > stock_maximo:
            messages.error(request, "Stock minimo no puede ser mayor al stock maximo.")
            return render(request, "productos/crear.html")
        if Producto.objects.filter(codigo=codigo).exists():
            messages.error(request, "YA existe un producto con ese codigo.")
            return render(request, "productos/crear.html")
        
        Producto.objects.create(codigo=codigo, nombre=nombre, categoria=categoria, stock=stock, stock_minimo=stock_minimo, stock_maximo=stock_maximo, precio=precio, activo=activo)

        messages.success(request, "Producto creado exitosamente.")
        return redirect("productos:listar_productos")
    

    return render(request, "productos/crear.html")


def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, "productos/listar.html", {"productos": productos})





def eliminar_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    if request.method == "POST":
        producto.delete()
        messages.success(request, f"Producto {producto.nombre} eliminado correctamente.")
        return redirect("productos:listar_productos")
    return render(request, "productos/eliminar.html",{"producto":producto})


def editar_producto(request, codigo):
    try:
        producto = Producto.objects.get(codigo=codigo)
    except Producto.DoesNotExist:
        messages.error(request, "Producto no encontrado.")
        return redirect("productos:listar_productos")

    if request.method == "POST":
        producto.nombre = request.POST.get("nombre")
        producto.categoria = request.POST.get("categoria")
        producto.stock = int(request.POST.get("stock"))
        producto.stock_minimo = int(request.POST.get("stock_minimo"))
        producto.stock_maximo = int(request.POST.get("stock_maximo"))
        producto.precio = float(request.POST.get("precio"))
        producto.activo = request.POST.get("activo") == "on"
        producto.save()
        messages.success(request, "Producto actualizado correctamente.")
        return redirect("productos:listar_productos")

    return render(request, "productos/editar.html", {"producto": producto})

# Create your views here.
