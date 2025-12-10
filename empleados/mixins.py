# Crear: empleados/mixins.py

from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        # Redirige si no está logueado O no es administrador
        if not request.user.is_authenticated or not request.user.es_administrador:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class CacheControlMixin:
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        # El decorador 'never_cache' agrega los encabezados Cache-Control y Pragma
        response = super().dispatch(*args, **kwargs)
        # Añadimos un encabezado extra para máxima compatibilidad
        response['Expires'] = '0' 
        return response