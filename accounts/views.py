# accounts/views.py (Código modificado para seguridad)

from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache # <--- Nuevo Import
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

class DashboardView(TemplateView):
    """
    Vista del Dashboard con verificación de autenticación y encabezados
    que prohíben el cacheo del navegador (previene la persistencia).
    """
    template_name = 'dashboard.html'
    
    # Aplica el decorador antes de que el método dispatch se ejecute
    @method_decorator(never_cache) 
    def dispatch(self, request, *args, **kwargs):
        # El IF de verificación de autenticación (TU CÓDIGO)
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('login')) 
            
        # Si está logueado, permite que la vista se ejecute
        return super().dispatch(request, *args, **kwargs)
    

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "registration/login.html", {"form": form})