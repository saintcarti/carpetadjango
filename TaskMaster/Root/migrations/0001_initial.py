# Generated by Django 5.1.2 on 2024-12-01 07:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            options={
                'db_table': 'Root_cliente',
            },
        ),
        migrations.CreateModel(
            name='productos',
            fields=[
                ('idProducto', models.AutoField(primary_key=True, serialize=False, verbose_name='Id producto')),
                ('nombreProducto', models.CharField(max_length=255, verbose_name='Nombre producto')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Precio producto')),
                ('imagen', models.ImageField(null=True, upload_to='imagenes', verbose_name='Imagen producto')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Stock producto')),
                ('categoria', models.CharField(blank=True, max_length=100, null=True, verbose_name='Categoría')),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Descuento (%)')),
            ],
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
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes', to='Root.cliente', verbose_name='Cliente')),
                ('productos', models.ManyToManyField(through='Root.DetalleSolicitud', to='Root.productos')),
            ],
        ),
        migrations.AddField(
            model_name='detallesolicitud',
            name='solicitud',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Root.solicitud'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('admin', 'Administrador'), ('supervisor', 'Supervisor'), ('vendedor', 'Vendedor')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('idTarea', models.AutoField(primary_key=True, serialize=False, verbose_name='Id tarea')),
                ('nombreTarea', models.CharField(max_length=100, verbose_name='Nombre tarea')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('fechaInicio', models.DateTimeField(auto_now_add=True, verbose_name='Fecha inicio')),
                ('fechaTermino', models.DateTimeField(blank=True, null=True, verbose_name='Fecha término')),
                ('horasDedicadas', models.PositiveIntegerField(default=0, verbose_name='Horas dedicadas')),
                ('notificado', models.BooleanField(default=False, verbose_name='Notificado')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Root.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='solicitud',
            name='vendedor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ventas', to='Root.userprofile', verbose_name='Vendedor'),
        ),
    ]
