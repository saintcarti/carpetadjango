from django import forms
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib.auth.password_validation import validate_password

class CustomUserCreationForm(forms.ModelForm):
    # Campo para seleccionar el grupo del usuario
    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=[role[0] for role in settings.ROLES]),
        required=True,
        label="Grupo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Campo para la contraseña
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="La contraseña debe tener al menos 8 caracteres."
    )
    
    # Campo para confirmar la contraseña
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Introduce nuevamente la contraseña para confirmar."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'group']

    # Validación de la primera contraseña
    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        validate_password(password)  # Valida la contraseña según las reglas de Django
        return password

    # Validación de la confirmación de la contraseña
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    # Guardar el usuario con su contraseña y grupo
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Establecer la contraseña de forma segura
        if commit:
            user.save()
            group = self.cleaned_data.get("group")
            if group:
                user.groups.add(group)  # Asignar el grupo al usuario
        return user
