from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages
from .forms import RegistroForm
from .models import Empleado
from django.contrib.auth.hashers import check_password
from .forms import RegistroForm, EmpleadoEditForm



# Decorador para proteger vistas
def empleado_session_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('empleado_id'):
            return redirect('/empleados/login/?next=' + request.path)
        return view_func(request, *args, **kwargs)
    return wrapper

# Registro de empleado
def listar_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados/listar.html', {'empleados': empleados})


def registrar_empleado(request):
    mensaje_error = ""
    
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                empleado = form.save(commit=False)  # No guardar aún
                empleado.set_password(form.cleaned_data['clave'])  # Aplica hash
                empleado.save()  # Ahora sí guarda con la contraseña hasheada
                return redirect("empleados:login")  # Redirige al login
            except IntegrityError:
                mensaje_error = "El usuario ya existe. Por favor, elige otro."
        else:
            mensaje_error = "Formulario inválido. Revisa los datos ingresados."
    else:
        form = RegistroForm()

    return render(request, "empleados/registrar.html", {"form": form, "mensaje_error": mensaje_error})

def editar_empleado(request, nombre_usuario):
    # Buscamos el empleado por nombre_usuario
    empleado = get_object_or_404(Empleado, nombre_usuario=nombre_usuario)
    
    if request.method == "POST":
        form = EmpleadoEditForm(request.POST, instance=empleado)  # <--- Cambiado
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado actualizado correctamente")
            return redirect("empleados:listar")
    else:
        form = EmpleadoEditForm(instance=empleado)  # <--- Cambiado

    return render(request, "empleados/editar.html", {"form": form, "empleado": empleado})

# Eliminar empleado
def eliminar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('empleados:listar')
    return render(request, 'empleados/eliminar.html', {'empleado': empleado})

def iniciar_sesion(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        clave = request.POST.get("clave")

        try:
            empleado = Empleado.objects.get(nombre_usuario=usuario)

            # Verificar la contraseña usando check_password (Django maneja PBKDF2)
            if check_password(clave, empleado.clave):
                # Guardar datos en sesión
                request.session['empleado_id'] = empleado.nombre_usuario
                request.session['empleado_cargo'] = empleado.cargo_trabajo
                if empleado.cargo_trabajo.lower() == 'administrador':

                    return redirect('/empleados/listar/')
                else:
                    return redirect('/inventario/productos/listar/')

            else:
                # Contraseña incorrecta
                return render(request, "empleados/login.html", {"error": "Usuario o clave incorrecta"})

        except Empleado.DoesNotExist:
            # Usuario no existe
            return render(request, "empleados/login.html", {"error": "Usuario o clave incorrecta"})

    # Si no es POST, mostrar formulario
    return render(request, "empleados/login.html")
def cerrar_sesion(request):
    request.session.flush()
    return redirect("empleados:login")