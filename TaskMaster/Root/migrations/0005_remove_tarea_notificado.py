# Generated by Django 5.1.2 on 2024-12-02 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Root', '0004_tarea_terminado_alter_cliente_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarea',
            name='notificado',
        ),
    ]
