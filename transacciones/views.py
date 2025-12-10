from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Movimiento
from .forms import MovimientoForm

class MovimientoListView(LoginRequiredMixin, ListView):
    model = Movimiento
    template_name = 'transacciones/movimiento_list.html'
    context_object_name = 'movimientos'

class MovimientoCreateView(LoginRequiredMixin, CreateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'transacciones/movimiento_form.html'
    success_url = reverse_lazy('movimiento_list')

    def form_valid(self, form):
        form.instance.responsable = self.request.user
        return super().form_valid(form)
