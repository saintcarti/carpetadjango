from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(UserProfile)

admin.site.register(Cliente)

admin.site.register(Solicitud)

admin.site.register(DetalleSolicitud)

admin.site.register(Tarea)

admin.site.register(productos)
