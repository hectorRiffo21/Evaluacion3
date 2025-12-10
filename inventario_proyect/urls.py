from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


from accounts.views import DashboardView

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('', redirect_to_login, name='home'),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')), 
    path('dashboard/', DashboardView.as_view(), name='dashboard'), 
    path('accounts/', include('accounts.urls')),
    path('empleados/', include('empleados.urls')),
    path('inventario/', include('inventario.urls')),
    path('movimientos/', include('transacciones.urls')),
]