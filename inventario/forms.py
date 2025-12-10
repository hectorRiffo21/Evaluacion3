from django import forms
from .models import Producto, Categoria

class ProductoForm(forms.ModelForm):

    categoria_nombre = forms.CharField(
        max_length=50, 
        required=True, 
        label="Categoría",
        help_text="Escribe el nombre de la categoría. Si ya existe, se asignará. Si no, se creará."
    )

    class Meta:
        model = Producto


        fields = ['nombre', 'codigo', 'stock', 'stock_minimo', 'stock_maximo', 'precio', 'descripcion', 'activo'] 


    def clean_categoria_nombre(self):
        nombre = self.cleaned_data['categoria_nombre'].strip()
        if not nombre:
            raise forms.ValidationError("La categoría no puede estar vacía.")
            

        categoria_obj, created = Categoria.objects.get_or_create(
            nombre__iexact=nombre,
            defaults={'nombre': nombre} 
        )

        return categoria_obj

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.categoria:
       
            self.fields['categoria_nombre'].initial = self.instance.categoria.nombre