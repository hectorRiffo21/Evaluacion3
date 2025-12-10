from django.db import models

class Categoria(models.Model):
    """Modelo para clasificar los productos."""
    nombre = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Categorías"

class Producto(models.Model):
    """
    Modelo ajustado para representar un producto en el inventario.
    """
    nombre = models.CharField(max_length=100, help_text="Nombre descriptivo del producto.")
    codigo = models.CharField(max_length=20, unique=True, help_text="Código único o SKU del producto.")
    
    # Stock
    stock = models.IntegerField(default=0, help_text="Cantidad actual en inventario.")
    stock_minimo = models.IntegerField(default=1, help_text="Nivel mínimo para generar alerta de reposición.")
    stock_maximo = models.IntegerField(default=9999, help_text="Nivel máximo deseado en inventario.")
    
    # Relación y Precios
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio de costo unitario.")
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    @property
    def valor_total(self):
        """Calcula el valor total del inventario para este producto (Stock * Precio)."""
        return self.stock * self.precio

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']