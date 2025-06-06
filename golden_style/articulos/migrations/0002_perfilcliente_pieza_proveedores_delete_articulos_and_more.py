# Generated by Django 5.2 on 2025-04-12 06:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articulos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254)),
                ('direccion_envio', models.TextField()),
                ('telefono', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Pieza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('descripcion', models.TextField()),
                ('talla', models.CharField(max_length=5)),
                ('color', models.CharField(max_length=50)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Proveedores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('contacto', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.DeleteModel(
            name='Articulos',
        ),
        migrations.AddField(
            model_name='pieza',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articulos.proveedores'),
        ),
    ]
