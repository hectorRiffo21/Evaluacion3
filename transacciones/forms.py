from django import forms
from .models import Movimiento

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['producto', 'tipo', 'cantidad', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Ej: Reposición, merma, robo, destrucción, ajuste...'
            })
        }
