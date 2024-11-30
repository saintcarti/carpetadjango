# Root/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    """
    Crea los grupos definidos en la configuración de roles
    después de aplicar las migraciones.
    """
    try:
        for role, _ in settings.ROLES:
            Group.objects.get_or_create(name=role)
    except Exception as e:
        print(f"Error al crear los grupos: {e}")
