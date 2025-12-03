from django import forms
from .models import Empleado

class RegistroForm(forms.ModelForm):
    confirmar_clave = forms.CharField(widget=forms.PasswordInput, label="Confirmar clave")

    class Meta:
        model = Empleado
        fields = [
            "nombre_usuario",
            "nombre",
            "apellido",
            "rut",
            "celular",
            "correo_electronico",
            "genero",
            "clave",
            "cargo_trabajo",
        ]
        widgets = {
            "clave": forms.PasswordInput(),
        }
        labels = {
            "clave": "Clave",
            "nombre_usuario": "Nombre de usuario",
        }

    def clean(self):
        cleaned_data = super().clean()
        clave = cleaned_data.get("clave")
        confirmar = cleaned_data.get("confirmar_clave")
        if clave != confirmar:
            self.add_error("confirmar_clave", "Las claves no coinciden")
