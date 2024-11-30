from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    role = models.CharField(max_length=20,choices=settings.ROLES)

def __str__(self):
    return self.user.username + ' - '+self.role
class Tarea(models.Model):
    idTarea = models.AutoField(primary_key=True, verbose_name='Id tarea')
    nombreTarea = models.CharField(max_length=100, verbose_name='Nombre tarea')
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    fechaInicio = models.DateTimeField(auto_now_add=True, verbose_name='Fecha inicio')
    fechaTermino = models.DateTimeField(verbose_name='Fecha término', null=True, blank=True)
    horasDedicadas = models.PositiveIntegerField(verbose_name='Horas dedicadas', default=0)
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    notificado = models.BooleanField(default=False, verbose_name='Notificado')

    def __str__(self):
        return self.nombreTarea

    
class productos(models.Model):
    idProducto = models.AutoField(primary_key=True,verbose_name='Id producto')
    nombreProducto = models.CharField(max_length=255,verbose_name='Nombre producto')
    precio = models.DecimalField(max_digits=5,decimal_places=2,verbose_name='Precio producto')
    imagen = models.ImageField(upload_to='imagenes',null=True,verbose_name='Imagen producto')
    stock = models.PositiveIntegerField(verbose_name='Stock producto',default=0)


class Cliente(models.Model):
    idCliente = models.AutoField(primary_key=True, verbose_name='Id cliente')
    nombre = models.CharField(max_length=100, verbose_name='Nombre del cliente')
    correo = models.EmailField(max_length=100, verbose_name='Correo del cliente')
    telefono = models.CharField(max_length=15, verbose_name='Teléfono del cliente', null=True, blank=True)
    direccion = models.TextField(verbose_name='Dirección del cliente', null=True, blank=True)
    contrato = models.DateField(verbose_name='Fecha de inicio del contrato', null=True, blank=True)
    duracion_contrato = models.PositiveIntegerField(verbose_name='Duración del contrato (meses)', null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Solicitud(models.Model):
    idSolicitud = models.AutoField(primary_key=True, verbose_name='Id solicitud')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    productos = models.ManyToManyField(productos, through='DetalleSolicitud')
    fechaSolicitud = models.DateTimeField(auto_now_add=True, verbose_name='Fecha solicitud')
    vendedor = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, verbose_name='Vendedor')

    def calcular_total(self):
        return sum(detalle.producto.precio * detalle.cantidad for detalle in self.detallesolicitud_set.all())
    
    def __str__(self):
        return f"Solicitud {self.idSolicitud} - {self.cliente.nombre}"



class DetalleSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    producto = models.ForeignKey(productos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombreProducto}"



