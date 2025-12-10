from django import forms
from .models import Empleado
from .utils import formatear_rut

GENERO_CHOICES = (
    ('Hombre', 'Hombre'),
    ('Mujer', 'Mujer'),
    ('Otro', 'Otro'),
    ('No Definido', 'No Definido'),
)

class EmpleadoForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label='Clave (Dejar vacío para no cambiar)'
    )

    genero = forms.ChoiceField(
        choices=GENERO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Empleado
        fields = ['nombre_usuario', 'password', 'correo_electronico', 
                  'nombre', 'apellido', 'rut', 'celular', 'genero', 
                  'cargo_trabajo']
        labels = {
            'nombre_usuario': 'Nombre de Usuario',
            'password': 'Clave (Dejar vacío para no cambiar)',
            'correo_electronico': 'Correo Electrónico',
            'cargo_trabajo': 'Cargo de Trabajo',
        }
        widgets = {
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo_trabajo': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilitar RUT al  momento de editar
        if self.instance and self.instance.pk:
            self.fields['rut'].disabled = True
        # dejar password vacío al mostrar el formulario
        self.fields['password'].initial = ''

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        return formatear_rut(rut)

    def save(self, commit=True):
        empleado = super().save(commit=False)
        password = self.cleaned_data.get("password")

        # Solo cambiar la contraseña si el usuario modifica el campo
        if password and password.strip():
            empleado.set_password(password)

        if commit:
            empleado.save()
        return empleado
