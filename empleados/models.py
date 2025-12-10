from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class EmpleadoManager(BaseUserManager):
    def create_user(self, nombre_usuario, correo_electronico, password=None, **extra_fields):
        if not correo_electronico:
            raise ValueError('El Empleado debe tener un correo electrónico válido')
        
        # Normaliza el email para consistencia
        email = self.normalize_email(correo_electronico)
        
        # Crea una instancia del modelo Empleado
        user = self.model(
            nombre_usuario=nombre_usuario,
            correo_electronico=email,
            **extra_fields
        )
        
        # Establece y hashea la clave del usuario
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre_usuario, correo_electronico, password=None, **extra_fields):
        # El súper usuario es un Administrador por defecto
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # se Establece el cargo
        extra_fields.setdefault('cargo_trabajo', 'Administrador') 
        
        # Validaciones de seguridad
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuario debe tener is_superuser=True.')

        return self.create_user(nombre_usuario, correo_electronico, password, **extra_fields)


CARGOS = (
    ('Administrador', 'Administrador'),
    ('Vendedor', 'Vendedor'),
    ('Bodeguero', 'Bodeguero'),
    ('Otro', 'Otro'),
)

class Empleado(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    rut = models.CharField(max_length=12, unique=True, verbose_name='RUT')
    celular = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')
    genero = models.CharField(max_length=20, blank=True, null=True, verbose_name='Género')
    nombre_usuario = models.CharField(max_length=150, unique=True, verbose_name='Nombre de Usuario')
    correo_electronico = models.EmailField(max_length=100, unique=True, verbose_name='Correo Electrónico')
    cargo_trabajo = models.CharField(max_length=50, choices=CARGOS, default='Vendedor', verbose_name='Cargo')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = EmpleadoManager()
    # Campo usado para iniciar sesión
    USERNAME_FIELD = 'nombre_usuario'
    # Campos requeridos al crear un usuario 
    REQUIRED_FIELDS = ['correo_electronico', 'nombre', 'apellido', 'rut'] 

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        
    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.cargo_trabajo})'
    

    def es_administrador(self):
        return self.cargo_trabajo == 'Administrador'