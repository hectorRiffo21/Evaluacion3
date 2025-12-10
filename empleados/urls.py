from django.urls import path
from . import views

urlpatterns = [
    # rutas crud admin
    path('', views.EmpleadoListView.as_view(), name='empleado_list'),
    path('crear/', views.EmpleadoCreateView.as_view(), name='empleado_create'),
    path('editar/<int:pk>/', views.EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('eliminar/<int:pk>/', views.EmpleadoDeleteView.as_view(), name='empleado_delete'),
    
    # rutas personal
    path('perfil/', views.PerfilDetalleView.as_view(), name='perfil_detalle'),
    path('perfil/editar/', views.PerfilUpdateView.as_view(), name='perfil_update'),
]