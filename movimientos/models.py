from django.db import models
from productos.models import Producto
from empleados.models import Empleado


class Movimiento(models.Model):
    tipo = models.CharField(max_length=20)
    codigo_producto = models.ForeignKey(Producto, on_delete= models.CASCADE)
    usuario_responsable = models.ForeignKey(Empleado, on_delete= models.SET_NULL, null=True)
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=200)
    stock_antes = models.IntegerField()
    stock_despues = models.IntegerField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_movimiento = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.tipo} - {self.codigo_producto} - {self.fecha_movimiento}"
# Create your models here.
