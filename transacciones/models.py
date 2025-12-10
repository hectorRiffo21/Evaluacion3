from django.db import models
from inventario.models import Producto
from django.contrib.auth import get_user_model

User = get_user_model()

class Movimiento(models.Model):
    TIPO_MOVIMIENTO = (
        ('ENTRADA', 'Entrada (Aumento de Stock)'),
        ('SALIDA', 'Salida (Disminución de Stock)'),
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='movimientos'
    )
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_MOVIMIENTO,
        verbose_name='Tipo de Movimiento'
    )
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    observaciones = models.TextField(blank=True, null=True)
    descripcion = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Indica el motivo del movimiento: compra, merma, robo, reposición, etc."
    )

    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"
        ordering = ['-fecha_movimiento']

    def __str__(self):
        return f"{self.tipo} de {self.cantidad} de {self.producto.nombre} - {self.descripcion or 'Sin descripción'}"

   
    def save(self, *args, **kwargs):
        # Solo actualizar stock si es un movimiento nuevo
        if not self.pk:
            if self.tipo == 'ENTRADA':
                self.producto.stock += self.cantidad
            else:  # SALIDA
                self.producto.stock -= self.cantidad
            self.producto.save()
        super().save(*args, **kwargs)
