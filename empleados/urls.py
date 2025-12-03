from django.urls import path
from . import views

app_name = 'empleados'

urlpatterns = [
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('registrar/', views.registrar_empleado, name='registrar'),
    path('listar/', views.listar_empleados, name='listar'),  # CRUD empleados
    path('editar/<str:nombre_usuario>/', views.editar_empleado, name='editar'),
    path('eliminar/<str:nombre_usuario>/', views.eliminar_empleado, name='eliminar'),
]
