from django.db import models
from django.db.models import Sum, Q
from estructura.models import Empresa, Equipo
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

class TipoRepuesto(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

class Repuesto(models.Model):
    nombre = models.CharField(max_length = 100)
    tipo_repuesto = models.ForeignKey(TipoRepuesto, on_delete=models.CASCADE)
    fabricante = models.CharField(max_length=50, null=True, blank=True)
    modelo = models.CharField(max_length=50, null=True, blank=True)
    # stock = models.IntegerField(default=0)
    # stock_minimo = models.IntegerField(default=0)
    es_critico = models.BooleanField(default=False)
    equipos = models.ManyToManyField(Equipo, related_name='repuestos')
    proveedores = models.ManyToManyField(Proveedor, related_name='repuestos')
    descatalogado = models.BooleanField(default=False)

    def stock(self):
        # print('calcula stock ...')
        s = Movimiento.objects.values('almacen__id', 'almacen__nombre', 'almacen__empresa__siglas', 'almacen__empresa__id').filter(Q(linea_pedido__repuesto=self) | Q(linea_inventario__repuesto=self)).annotate(suma=Sum('cantidad')) #['suma'] or 0
        # ajustes = Movimiento.objects.filter(linea_inventario__repuesto=self).aggregate(suma=Sum('cantidad'))['suma'] or 0
        
        return s #entradas + ajustes

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(default=timezone.now)
    fecha_entrega = models.DateField(blank=True, null=True)
    
    def completo(self):
        lineas_pendientes = LineaPedido.objects.filter(pedido=self).filter(completo=False).count()
        return lineas_pendientes == 0


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

    def completo(self):
        return self.pendiente() <= 0

class Almacen(models.Model):
    nombre = models.CharField(max_length=100)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def empresa_siglas(self):
        return self.empresa.siglas

    def __str__(self):
        return self.nombre

class StockMinimo(models.Model):
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE, related_name='stocks_minimos')
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, related_name='stocks_minimos')
    cantidad = models.IntegerField()

    def __str__(self):
        return self.repuesto.nombre

class Inventario(models.Model):
    nombre = models.CharField(max_length = 100, default='Ajuste inicial')
    fecha_creacion = models.DateField(default=timezone.now)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre + ' - ' + str(self.fecha_creacion)

class LineaInventario(models.Model):
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)

class Movimiento(models.Model):
    fecha = models.DateField(default=timezone.now)
    cantidad = models.IntegerField()
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    linea_pedido = models.ForeignKey(LineaPedido, on_delete=models.CASCADE, blank=True, null=True)
    linea_inventario = models.ForeignKey(LineaInventario, on_delete=models.CASCADE, blank=True, null=True)

class Foto(models.Model):
    imagen = models.ImageField(upload_to='equipos')
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)