from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Empleado(models.Model):
    nombre_usuario = models.CharField(max_length=50, primary_key=True)  # <--- clave primaria
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    rut = models.CharField(max_length=12)
    celular = models.CharField(max_length=15)
    correo_electronico = models.CharField(max_length=100)
    genero = models.CharField(max_length=20)
    clave = models.CharField(max_length=255)
    cargo_trabajo = models.CharField(max_length=50)

    def set_password(self, raw_password):
        self.clave = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.clave)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.nombre_usuario})"

    class Meta:
        db_table = 'empleados'
        managed = False  # Django no intentará crear ni modificar la tabla
