from django.db import models
from django.contrib.auth.models import User

class Almacen(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Almacén"
        verbose_name_plural = "Almacenes"

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo_barras = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre

class Recepcion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    proveedor = models.CharField(max_length=150)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Recepción"
        verbose_name_plural = "Recepciones"

    def __str__(self):
        return f"Recepción de {self.producto.nombre}"

class Despacho(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    destino = models.CharField(max_length=200)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    fecha_despacho = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Despacho"
        verbose_name_plural = "Despachos"

    def __str__(self):
        return f"Despacho a {self.destino}"

class PerfilUsuario(models.Model):
    MODULOS_CHOICES = [
        ('catalogo', 'Catálogo'),
        ('almacen', 'Almacén'),
        ('inventario', 'Inventario'),
        ('recepcion', 'Recepción'),
        ('despacho', 'Despacho'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    modulo_asignado = models.CharField(max_length=50, choices=MODULOS_CHOICES)

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"

    def __str__(self):
        return f"{self.user.username} - {self.modulo_asignado}"

class Trazabilidad(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    ubicacion_actual = models.CharField(max_length=200, verbose_name="Ubicación Actual")
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Latitud")
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Longitud")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    class Meta:
        verbose_name = "Trazabilidad"
        verbose_name_plural = "Trazabilidades"

    def __str__(self):
        return f"{self.producto.nombre} - {self.ubicacion_actual}"