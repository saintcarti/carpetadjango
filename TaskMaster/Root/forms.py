from django import forms
from django.contrib.auth.models import User, Group
from django.conf import settings

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
