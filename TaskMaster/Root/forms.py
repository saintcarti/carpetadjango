from django import forms
from django.contrib.auth.models import User, Group
from django.conf import settings
from .models import Solicitud, DetalleSolicitud,productos,Cliente,UserProfile,Tarea


class CustomUserCreationForm(forms.ModelForm):
    # Campo para seleccionar el grupo de usuario (Administrador, Supervisor, Vendedor)
    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=[role[0] for role in settings.ROLES]),  # Filtrando según los roles definidos en settings.ROLES
        required=True,
        label="Grupo",
        widget=forms.Select(attrs={'class': 'form-control'})  # Asegurando el estilo de Bootstrap
    )

    # Campos para contraseña
    password1 = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'group']  # Los campos que se deben mostrar en el formulario

    # Validación de la confirmación de contraseña
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    # Método para guardar al usuario y asignar el grupo seleccionado
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()  # Guarda el usuario en la base de datos
            group = self.cleaned_data["group"]
            user.groups.add(group)  # Asigna el grupo al usuario

            # Si el grupo es 'admin', asignamos privilegios de staff y superusuario
            if group.name == 'admin':
                user.is_staff = True
                user.is_superuser = True
                user.save()

        return user


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['cliente', 'vendedor', 'productos']  # Los campos que quieres que el formulario maneje

    # Cliente (campo de selección único)
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(), 
        empty_label="Seleccione un cliente", 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Vendedor (campo de selección único)
    vendedor = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(role='vendedor'), 
        empty_label="Seleccione un vendedor", 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Productos (campo de selección único)
    productos = forms.ModelChoiceField(
        queryset=productos.objects.all(), 
        empty_label="Seleccione un producto", 
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class DetalleSolicitudForm(forms.ModelForm):
    class Meta:
        model = DetalleSolicitud
        fields = ['producto', 'cantidad']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = productos
        fields = ['imagen', 'nombreProducto', 'precio', 'stock', 'descuento']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['nombreTarea', 'descripcion', 'fechaTermino', 'horasDedicadas', 'usuario', 'terminado']
        widgets = {
            'nombreTarea': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'fechaTermino': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'horasDedicadas': forms.NumberInput(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),  # Para seleccionar el usuario asignado
            'terminado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }