from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.
class usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True ,verbose_name='Id usuario')
    nombreUsuario = models.CharField(max_length=20,verbose_name='Nombre usuario')
    correo = models.EmailField(max_length=50,verbose_name='Correo usuario')
    contrasena = models.CharField(max_length=255,verbose_name='Contrasena usuario')
    contrasena2 = models.CharField(max_length=255,verbose_name='Contrasena usuario 2')

    def __str__(self):
        return self.nombreUsuario
    
class tarea(models.Model):
    idTarea = models.AutoField(primary_key=True, verbose_name='Id tarea')
    nombreTarea = models.CharField(max_length=100,verbose_name='Nombre tarea')
    fechaInicio = models.DateTimeField(auto_now_add=True, verbose_name='Fecha inicio')
    fechaTermino = models.DateTimeField(verbose_name='Fecha término', null=True, blank=True)
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreTarea
    
class productos(models.Model):
    idProducto = models.AutoField(primary_key=True,verbose_name='Id producto')
    nombreProducto = models.CharField(max_length=255,verbose_name='Nombre producto')
    precio = models.DecimalField(max_digits=5,decimal_places=2,verbose_name='Precio producto')
    imagen = models.ImageField(upload_to='imagenes',null=True,verbose_name='Imagen producto')
    stock = models.PositiveIntegerField(verbose_name='Stock producto',default=0)


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    role = models.CharField(max_length=20,choices=settings.ROLES)

    def __str__(self):
        return self.user.username + ' - '+self.role