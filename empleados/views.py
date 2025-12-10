from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.hashers import make_password 
from .models import Empleado
from .forms import EmpleadoForm
from .mixins import AdminRequiredMixin, CacheControlMixin 
from django.shortcuts import get_object_or_404 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render



# Listar los empleados
class EmpleadoListView(LoginRequiredMixin, AdminRequiredMixin, CacheControlMixin, ListView):
    model = Empleado
    template_name = 'empleados/empleado_list.html' 
    context_object_name = 'empleados' 
    paginate_by = 10 

# Crear empleado
class EmpleadoCreateView(LoginRequiredMixin, AdminRequiredMixin, CacheControlMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleados/empleado_form.html'
    success_url = reverse_lazy('empleado_list') 

    # Sobreescribir form_valid para hashear la contraseña solo en la creación
    def form_valid(self, form):
        nueva_contrasena = form.cleaned_data.get('password')
        if nueva_contrasena:
            # Hashear y guardar la contraseña nueva
            form.instance.password = make_password(nueva_contrasena)
        return super().form_valid(form)

# actualizar empleado
class EmpleadoUpdateView(LoginRequiredMixin, AdminRequiredMixin, CacheControlMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleados/empleado_form.html'
    success_url = reverse_lazy('empleado_list') 
    cancel_url = reverse_lazy('empleado_list')
    
    # Previene que se exija la contraseña al editar
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if form.instance.pk:

             if not form.instance.password: 
                 form.fields['password'].required = False
             else:
                 form.fields['password'].required = False
        return form


    def form_valid(self, form):
        empleado_instance = form.instance
        nueva_contrasena = form.cleaned_data.get('password')


        if nueva_contrasena and nueva_contrasena not in [empleado_instance.password, '']: 
            empleado_instance.password = make_password(nueva_contrasena)
        else:

            empleado_instance.password = self.get_object().password

        return super().form_valid(form)


# eliminar empleado
class EmpleadoDeleteView(LoginRequiredMixin, AdminRequiredMixin, CacheControlMixin, DeleteView):
    model = Empleado
    template_name = 'empleados/empleado_confirm_delete.html'
    context_object_name = 'empleado' 
    success_url = reverse_lazy('empleado_list') 



# editar mi propio perfil
class PerfilUpdateView(LoginRequiredMixin, CacheControlMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleados/empleado_form.html'
    success_url = reverse_lazy('dashboard') 
    cancel_url = reverse_lazy('dashboard')
    
    def get_object(self, queryset=None):
        
        return self.request.user
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('cargo_trabajo', None)
        if 'password' in form.fields:
            form.fields['password'].required = False
        return form
    
    def form_valid(self, form):
        empleado_instance = form.instance
        nueva_contrasena = form.cleaned_data.get('password')


        empleado_original = Empleado.objects.get(pk=empleado_instance.pk)

        if nueva_contrasena:

            empleado_instance.password = make_password(nueva_contrasena)
        else:

            empleado_instance.password = empleado_original.password

        return super().form_valid(form)
    
class PerfilDetalleView(LoginRequiredMixin, CacheControlMixin, DetailView):
    model = Empleado
    template_name = 'empleados/perfil_detalle.html' 
    context_object_name = 'empleado'

    def get_object(self, queryset=None):
        return self.request.user