from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from .models import (
    Proveedores, Categoria, Carrito, Pedido,
    PedidoDetalle, Usuario, Productos
)

# Acción personalizada para convertir carritos en pedido
@admin.action(description="Convertir en pedido y vaciar carrito")
def convertir_en_pedido(modeladmin, request, queryset):
    usuarios = set(queryset.values_list('usuario', flat=True))

    for usuario_id in usuarios:
        usuario = Usuario.objects.get(id=usuario_id)
        items_usuario = queryset.filter(usuario=usuario)

        if not items_usuario.exists():
            continue

        total = sum(item.producto.precio * item.cantidad for item in items_usuario)

        pedido = Pedido.objects.create(
            usuario=usuario,
            total=total,
            estado='pendiente',
            fecha=timezone.now()
        )

        pedido.numero_pedido = f"PED-{pedido.id:06d}"
        pedido.save()

        for item in items_usuario:
            PedidoDetalle.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio,
                subtotal=item.producto.precio * item.cantidad
            )

            item.producto.stock -= item.cantidad
            item.producto.save()

        items_usuario.delete()

        messages.success(request, f"Pedido {pedido.numero_pedido} creado para {usuario.nombre_completo}")


# Registros normales
admin.site.register(Proveedores)
admin.site.register(Categoria)
admin.site.register(Pedido)
admin.site.register(PedidoDetalle)
admin.site.register(Usuario)
admin.site.register(Productos)

# Registro de Carrito con acción personalizada
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'cantidad')
    actions = [convertir_en_pedido]
