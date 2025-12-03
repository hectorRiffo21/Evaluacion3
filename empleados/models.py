from django.db import models
class Empleado(models.Model):
    nombre_usuario = models.CharField(primary_key=True, max_length=50)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    rut = models.CharField(max_length=12)
    celular = models.CharField(max_length=20)
    correo_electronico = models.CharField(max_length=50)
    genero = models.CharField(max_length=10)
    clave = models.TextField()
    cargo_trabajo = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.nombre_usuario})"

# Create your models here.
