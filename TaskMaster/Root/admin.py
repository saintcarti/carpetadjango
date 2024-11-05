from django.contrib import admin
from .models import usuario,tarea,productos
# Register your models here.

admin.site.register(usuario)

admin.site.register(tarea)

admin.site.register(productos)
