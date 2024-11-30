# Generated by Django 5.1.2 on 2024-11-29 21:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Root', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('idCliente', models.AutoField(primary_key=True, serialize=False, verbose_name='Id cliente')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del cliente')),
                ('correo', models.EmailField(max_length=100, verbose_name='Correo del cliente')),
                ('telefono', models.CharField(blank=True, max_length=15, null=True, verbose_name='Teléfono del cliente')),
                ('direccion', models.TextField(blank=True, null=True, verbose_name='Dirección del cliente')),
                ('contrato', models.DateField(blank=True, null=True, verbose_name='Fecha de inicio del contrato')),
                ('duracion_contrato', models.PositiveIntegerField(blank=True, null=True, verbose_name='Duración del contrato (meses)')),
            ],
        ),
        migrations.AlterField(
            model_name='tarea',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Root.userprofile'),
        ),
        migrations.AddField(
            model_name='tarea',
            name='descripcion',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AddField(
            model_name='tarea',
            name='horasDedicadas',
            field=models.PositiveIntegerField(default=0, verbose_name='Horas dedicadas'),
        ),
        migrations.AddField(
            model_name='tarea',
            name='notificado',
            field=models.BooleanField(default=False, verbose_name='Notificado'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('admin', 'Administrador'), ('cliente', 'Cliente'), ('vendedor', 'Vendedor'), ('supervisor', 'Supervisor')], max_length=20),
        ),
        migrations.CreateModel(
            name='DetalleSolicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(verbose_name='Cantidad')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Root.productos')),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('idSolicitud', models.AutoField(primary_key=True, serialize=False, verbose_name='Id solicitud')),
                ('fechaSolicitud', models.DateTimeField(auto_now_add=True, verbose_name='Fecha solicitud')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Root.cliente', verbose_name='Cliente')),
                ('productos', models.ManyToManyField(through='Root.DetalleSolicitud', to='Root.productos')),
                ('vendedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Root.userprofile', verbose_name='Vendedor')),
            ],
        ),
        migrations.AddField(
            model_name='detallesolicitud',
            name='solicitud',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Root.solicitud'),
        ),
        migrations.DeleteModel(
            name='usuario',
        ),
    ]