from django.db import models

class Producto(models.Model):
    codigo = models.CharField(primary_key=True, max_length=50)
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, blank=True,null=True)
    stock = models.IntegerField()
    stock_minimo = models.IntegerField()
    stock_maximo = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
# Create your models here.
