from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from inventario.models import Producto
from .models import Movimiento

