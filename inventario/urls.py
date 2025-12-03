from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path(' productos/listar/', views.listar_productos, name='listar_productos'),
    path(' productos/crear/', views.crear_producto, name='crear_producto'),
]
