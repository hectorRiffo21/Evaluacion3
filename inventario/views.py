from django.shortcuts import render, redirect
from functools import wraps
from productos.models import Producto

# decorador para proteger vistas según tu sesión
def empleado_session_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('empleado_id'):
            return redirect('/empleados/login/?next=' + request.path)
        return view_func(request, *args, **kwargs)
    return wrapper

# Vista de inicio
@empleado_session_required  # <- CAMBIO AQUÍ: antes estaba @empleado_login_required (no existe)
def inicio(request):
    return render(request, "inventario/inicio.html")

# Crear producto
@empleado_session_required  # <- proteger también esta vista
def crear_producto(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        nombre = request.POST.get("nombre")
        categoria = request.POST.get("categoria")
        stock = request.POST.get("stock")
        stock_minimo = request.POST.get("stock_minimo")
        stock_maximo = request.POST.get("stock_maximo")
        precio = request.POST.get("precio")

        Producto.objects.create(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            stock=stock,
            stock_minimo=stock_minimo,
            stock_maximo=stock_maximo,
            precio=precio
        )
        return redirect("inventario:listar_productos")  # <- usar namespace y nombre de URL

    return render(request, "productos/crear.html")

# Listar productos
@empleado_session_required  # <- CAMBIO: quitar @login_required de Django
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, "productos/listar.html", {"productos": productos})