from django.urls import path
from . import views

urlpatterns = [
    # Productos
    path('', views.ProductoListView.as_view(), name='inventario_list'),
    path('crear/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('editar/<int:pk>/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('eliminar/<int:pk>/', views.ProductoDeleteView.as_view(), name='producto_delete'),

    # Productos eliminados
    path('eliminados/', views.ProductoEliminadoListView.as_view(), name='producto_eliminado_list'),
    path('activar/<int:pk>/', views.ProductoActivarView.as_view(), name='producto_activar'),

    # Categorías
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/crear/', views.CategoriaCreateView.as_view(), name='categoria_create'),
]
