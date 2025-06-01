from django.db import models
from django.utils import timezone

# Categoría debe estar arriba en caso de que luego se use como ForeignKey en otros modelos
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Proveedores(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=100)
    correo = models.EmailField()
    direccion_envio = models.TextField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre_completo

class Productos(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    talla = models.CharField(max_length=5)  # Ej: S, M, L, XL
    color = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    # categoría = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)  # opcional

    def __str__(self):
        return f"{self.nombre} - {self.talla} - {self.color}"

class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'producto')

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.usuario} - {self.producto} ({self.cantidad})"

class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('procesado', 'Procesado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ]
    numero_pedido = models.CharField(max_length=20, unique=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def save(self, *args, **kwargs):
        if not self.numero_pedido:
            ultimo_pedido = Pedido.objects.order_by('-id').first()
            if ultimo_pedido and ultimo_pedido.numero_pedido:
                try:
                    ultimo_numero = int(ultimo_pedido.numero_pedido.split('-')[1])
                    nuevo_numero = ultimo_numero + 1
                except (IndexError, ValueError):
                    nuevo_numero = 1
            else:
                nuevo_numero = 1
            self.numero_pedido = f"PED-{nuevo_numero:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.numero_pedido} - {self.usuario}"

class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto} x {self.cantidad} (Pedido {self.pedido.numero_pedido})"
