from django.db import models
from productos.models import Producto
from empleados.models import Empleado




class Movimiento(models.Model):
    descripcion = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario_responsable = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.descripcion} - {self.usuario_responsable}"
