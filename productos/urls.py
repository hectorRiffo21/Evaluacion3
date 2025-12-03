from django.urls import path
from . import views

app_name = "productos"

urlpatterns = [
    path("crear/", views.crear_producto, name="crear_producto"),
    path("listar/", views.listar_productos, name="listar_productos"),
    path("eliminar/<str:codigo>/", views.eliminar_producto, name="eliminar_producto"),
    path("editar/<str:codigo>/", views.editar_producto, name="editar_producto")
]
