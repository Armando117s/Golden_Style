# Generated by Django 5.1.6 on 2025-06-01 02:50

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articulos', '0003_rename_pieza_productos_rename_perfilcliente_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_pedido', models.CharField(blank=True, max_length=20, unique=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('procesado', 'Procesado'), ('enviado', 'Enviado'), ('entregado', 'Entregado')], default='pendiente', max_length=20)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articulos.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='articulos.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articulos.productos')),
            ],
        ),
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('fecha_agregado', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articulos.productos')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articulos.usuario')),
            ],
            options={
                'unique_together': {('usuario', 'producto')},
            },
        ),
    ]
