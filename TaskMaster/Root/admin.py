from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(UserProfile)

admin.site.register(Cliente)

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('idSolicitud', 'cliente', 'vendedor', 'fechaSolicitud',)
    search_fields = ('cliente__nombre', 'vendedor__user__username')
    list_filter = ('fechaSolicitud',)

admin.site.register(DetalleSolicitud)

admin.site.register(Tarea)

admin.site.register(productos)
