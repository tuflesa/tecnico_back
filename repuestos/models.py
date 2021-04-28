from django.db import models
from estructura.models import Equipo
from django.utils import timezone
from django.contrib.auth.models import User

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    correo_electronico = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + ' ' + self.proveedor.nombre 

class Repuesto(models.Model):
    nombre = models.CharField(max_length = 100)
    fabricante = models.CharField(max_length=50, null=True, blank=True)
    modelo = models.CharField(max_length=50, null=True, blank=True)
    stock = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)
    es_critico = models.BooleanField(default=False)
    equipos = models.ManyToManyField(Equipo)
    proveedores = models.ManyToManyField(Proveedor)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(default=timezone.now)
    fecha_entrega = models.DateField(blank=True, null=True)
    completo = models.BooleanField(default=False)

class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def pendiente(self):
        sum = 0
        movimientos = Movimiento.objects.filter(linea_pedido=self)
        for movimiento in movimientos:
            sum += movimiento.cantidad
        return self.cantidad - sum

class Inventario(models.Model):
    fecha = models.DateField(default=timezone.now)
    cantidad = models.IntegerField()
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL)

class Movimiento(models.Model):
    fecha = models.DateField(default=timezone.now)
    cantidad = models.IntegerField()
    linea_pedido = models.ForeignKey(LineaPedido, on_delete=models.CASCADE, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

class Foto(models.Model):
    imagen = models.ImageField(upload_to='equipos')
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)