from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import ProtectedError
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.db import transaction 

from transacciones.models import Movimiento
from .models import Producto, Categoria
from empleados.mixins import AdminRequiredMixin
from .forms import ProductoForm




class ProductoListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Producto
    template_name = 'inventario/producto_list.html'
    context_object_name = 'productos'

    def get_queryset(self):

        return Producto.objects.filter(activo=True)


class ProductoCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Producto
    template_name = 'inventario/producto_form.html'
    form_class = ProductoForm
    success_url = reverse_lazy('inventario_list') 

    def form_valid(self, form):

        categoria_obj = form.cleaned_data['categoria_nombre']
        form.instance.categoria = categoria_obj
        
  
        response = super().form_valid(form)

     
     
        if self.object.stock > 0:
            Movimiento.objects.create(
                producto=self.object,
                tipo='ENTRADA',
                cantidad=self.object.stock,
                responsable=self.request.user,
               
                descripcion='Registro inicial del producto en inventario.'
            )
        return response


class ProductoUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Producto
    template_name = 'inventario/producto_form.html'
    form_class = ProductoForm
  
    success_url = reverse_lazy('inventario_list')

    def form_valid(self, form):
        with transaction.atomic():
            producto_original = self.get_object()
            stock_original = producto_original.stock
            response = super().form_valid(form)
            stock_nuevo = self.object.stock
            diff = stock_nuevo - stock_original

            if diff != 0:
                Movimiento.objects.create(
                    producto=self.object,
                    tipo='ENTRADA' if diff > 0 else 'SALIDA',
                    cantidad=abs(diff),
                    responsable=self.request.user,
                    descripcion=f"Ajuste de stock: {stock_original} → {stock_nuevo}"
                )
            elif form.has_changed():
                Movimiento.objects.create(
                    producto=self.object,
                    tipo='ENTRADA',  
                    cantidad=0,
                    responsable=self.request.user,
                    descripcion="Edición de datos del producto (sin cambio de stock)"
                )
            return response



class ProductoDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Producto
    template_name = 'inventario/producto_confirm_delete.html'
    success_url = reverse_lazy('inventario_list')

    def form_valid(self, form):
        self.object = self.get_object()

     
        Movimiento.objects.create(
            producto=self.object,
            tipo='SALIDA',
            cantidad=self.object.stock,
            responsable=self.request.user,
            descripcion=f"Producto '{self.object.nombre}' desactivado"
        )


        self.object.activo = False
        self.object.save()

        messages.success(self.request, f"Producto '{self.object.nombre}' desactivado con éxito.")
        return redirect(self.success_url)




class CategoriaListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Categoria
    template_name = 'inventario/categoria_list.html'
    context_object_name = 'categorias'


class CategoriaCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Categoria
    template_name = 'inventario/categoria_form.html'
    fields = ['nombre']
    success_url = reverse_lazy('categoria_list')


class CategoriaDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'inventario/categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, f"Categoría '{self.object.nombre}' eliminada con éxito.")
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(
                request,
                f"No se puede eliminar la categoría '{self.object.nombre}' porque tiene productos asociados. Elimine los productos primero."
            )
            return redirect(self.success_url)





class ProductoEliminadoListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Producto
    template_name = 'inventario/producto_eliminado_list.html'
    context_object_name = 'productos'

    def get_queryset(self):
        return Producto.objects.filter(activo=False)


class ProductoActivarView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        with transaction.atomic():
            producto = Producto.objects.get(pk=pk)
            stock_anterior = producto.stock

            producto.activo = True
            producto.stock = 0  
            producto.save()

          
            Movimiento.objects.create(
                producto=producto,
                tipo='ENTRADA',
                cantidad=0,
                responsable=request.user,
                descripcion=f"Producto '{producto.nombre}' activado. Stock anterior: {stock_anterior}"
            )

            messages.success(request, f"Producto '{producto.nombre}' activado correctamente.")
            return redirect('producto_eliminado_list')
