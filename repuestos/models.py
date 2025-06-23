from django.db import models
from django.db.models import Sum, Q
from django.db.models.deletion import CASCADE
from estructura.models import Empresa, Equipo, Direcciones
from mantenimiento.models import ParteTrabajo
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    direccion = models.TextField(max_length=250, blank=True, null=True)
    poblacion = models.TextField(max_length=75, blank=True, null=True)
    condicion_pago = models.CharField(max_length=200, blank=True, null=True)
    condicion_entrega = models.CharField(max_length=50, blank=True, null=True)
    cif = models.CharField(max_length=12, blank=True, null=True)
    pais = models.TextField(max_length=75, default='España')
    cod_ekon = models.TextField(max_length=8, blank=True, null=True)
    de_rectificado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    correo_electronico = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='contactos')

    def __str__(self):
        return self.nombre + ' ' + self.proveedor.nombre 

class TipoRepuesto(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

class TipoUnidad(models.Model):
    nombre = models.CharField(max_length=30)
    siglas = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

class Repuesto(models.Model):
    nombre = models.CharField(max_length = 150)
    tipo_repuesto = models.ForeignKey(TipoRepuesto, on_delete=models.CASCADE)
    tipo_unidad = models.ForeignKey(TipoUnidad, on_delete=models.PROTECT, default=1)
    fabricante = models.CharField(max_length=50, null=True, blank=True)
    modelo = models.CharField(max_length=90, null=True, blank=True)
    # stock = models.IntegerField(default=0)
    # stock_minimo = models.IntegerField(default=0)
    es_critico = models.BooleanField(default=False)
    equipos = models.ManyToManyField(Equipo, related_name='repuestos', blank=True)
    proveedores = models.ManyToManyField(Proveedor, blank=True, related_name='repuestos')
    descatalogado = models.BooleanField(default=False)
    observaciones = models.CharField(max_length=300, null=True, blank=True)
    nombre_comun = models.CharField(max_length = 100, null=True, blank=True)

    #def stock(self):
        # print('calcula stock ...')
        #s = Movimiento.objects.values('almacen__id', 'almacen__nombre', 'almacen__empresa__siglas', 'almacen__empresa__id').filter(Q(linea_pedido__repuesto=self) | Q(linea_inventario__repuesto=self)).annotate(suma=Sum('cantidad')) #['suma'] or 0
        # ajustes = Movimiento.objects.filter(linea_inventario__repuesto=self).aggregate(suma=Sum('cantidad'))['suma'] or 0
        
        #return s #entradas + ajustes
    def unidad_nombre(self):
            return self.tipo_unidad.nombre

    def unidad_siglas(self):
            return self.tipo_unidad.siglas

    def __str__(self):
        return self.nombre

class ContadorPedidos(models.Model):
    year = models.IntegerField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    contador = models.IntegerField(default=0)

    def __str__(self):
        return str(self.year) + '-' + str(self.contador)

class Pedido(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(default=timezone.now)
    fecha_entrega = models.DateField(blank=True, null=True)
    fecha_prevista_entrega = models.DateField(blank=True, null=True)
    finalizado = models.BooleanField(default=False)
    numero = models.CharField(max_length=12, null=True, blank=True, default=None)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    direccion_envio = models.ForeignKey(Direcciones, on_delete= models.SET_NULL, null= True, blank= True)
    contacto = models.ForeignKey(Contacto, on_delete=models.SET_NULL, null= True, blank=True)
    observaciones = models.CharField(max_length=500, null=True, blank=True)
    observaciones2 = models.CharField(max_length=500, null=True, blank=True)
    descripcion = models.CharField(max_length=300, null=False, blank=False)
    intervencion = models.BooleanField(default=False, null=True, blank=True)
    revisado = models.BooleanField(default=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generar nuevo número si el campo numero es None (null)
        if self.numero is None:
            currentDateTime = datetime.datetime.now()
            date = currentDateTime.date()
            year = date.strftime("%Y")

            contador = ContadorPedidos.objects.filter(year=year, empresa=self.empresa)
            if (len(contador)==0):
                contador = ContadorPedidos(year=year, contador=0, empresa=self.empresa)
                contador.save()
                numero=1
            else:
                contador = ContadorPedidos.objects.get(year=year, empresa=self.empresa)
                numero=contador.contador+1

            contador.contador = numero
            contador.save()

            self.numero = self.empresa.siglas + '-' + year + '-' + str(numero).zfill(3)
        # Llamar al metodo save por defecto de la clase
        super(Pedido,self).save(*args, **kwargs)

    
    """ def es_completo(self):
        lineas_pendientes = LineaPedido.objects.filter(pedido=self).filter(completo=False).count()
        lineas_adicionales_pendientes = LineaAdicional.objects.filter(pedido=self).filter(completo=False).count()
        return (lineas_pendientes + lineas_adicionales_pendientes) == 0 """


class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas_pedido')
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE, related_name='lineas_repuesto')
    descripcion_proveedor = models.CharField(max_length = 150, blank= True, null=True)
    modelo_proveedor = models.CharField(max_length=90, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=13, decimal_places=4, blank=True, null=True)
    por_recibir = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, blank= True, null=True)
    total = models.DecimalField(max_digits=13, decimal_places=4, blank=True, null=True)
    tipo_unidad = models.ForeignKey(TipoUnidad, on_delete=models.PROTECT, default=1)
   
class LineaAdicional(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas_adicionales')
    descripcion = models.CharField(max_length=250)
    cantidad = models.DecimalField(max_digits=13, decimal_places=2)
    precio = models.DecimalField(max_digits=13, decimal_places=4, blank=True, null=True)
    por_recibir = models.DecimalField(max_digits=13, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, blank= True, null=True)
    total = models.DecimalField(max_digits=13, decimal_places=4, blank=True, null=True)

    """ def pendiente(self):
        sum = 0
        entregas = Entrega.objects.filter(linea_adicional=self)
        for entrega in entregas:
            sum += entrega.cantidad
        return self.cantidad - sum

    def completo(self):
        return self.pendiente() <= 0 """

class Entrega(models.Model):
    linea_adicional = models.ForeignKey(LineaAdicional, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    cantidad = models.DecimalField(max_digits=13, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    albaran = models.CharField(max_length=50, null=True, blank=True, default='')

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
    cantidad = models.DecimalField(max_digits=13, decimal_places=2, default=0) #cantidad mínima, stock mínimo del repuesto si este es crítico
    cantidad_aconsejable = models.DecimalField(max_digits=13, decimal_places=2, default=0) #cantidad mínima de stock aconsejable cuando no es crítico
    localizacion = models.CharField(max_length=50, null=True, blank=True)
    stock_act = models.DecimalField(max_digits=13, decimal_places=2, default=0)

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
    cantidad = models.DecimalField(max_digits=13, decimal_places=2, default=0)

class Salida(models.Model):
    nombre = models.CharField(max_length = 100, default='Salida almacén')
    fecha_creacion = models.DateField(default=datetime.date.today)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    num_parte = models.ForeignKey(ParteTrabajo, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre + ' - ' + str(self.fecha_creacion)

class LineaSalida(models.Model):
    salida = models.ForeignKey(Salida, on_delete=models.CASCADE, related_name='lineas')
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=13, decimal_places=2, default=0)

class Movimiento(models.Model):
    fecha = models.DateField(default=datetime.date.today)
    cantidad = models.DecimalField(max_digits=13, decimal_places=2)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    linea_pedido = models.ForeignKey(LineaPedido, on_delete=models.CASCADE, blank=True, null=True, related_name='movimiento')
    linea_inventario = models.ForeignKey(LineaInventario, on_delete=models.CASCADE, blank=True, null=True)
    linea_salida = models.ForeignKey(LineaSalida, on_delete=models.CASCADE, blank=True, null=True)
    albaran = models.CharField(max_length=50, null=True, blank=True, default='')

    def save(self, *args, **kwargs):
        if self.linea_pedido != None:
            # print(self.linea_pedido.id)
            linea = LineaPedido.objects.get(id=self.linea_pedido.id)
            # print(linea.repuesto)
            
        if self.linea_inventario != None:
            # print(self.linea_inventario.id)
            linea = LineaInventario.objects.get(id=self.linea_inventario.id)
            #print(linea.repuesto)
    
        if self.linea_salida != None:
            # print(self.linea_salida.id)
            linea = LineaSalida.objects.get(id=self.linea_salida.id)
            # print(linea.repuesto)

        stock = StockMinimo.objects.get(repuesto=linea.repuesto, almacen=self.almacen)
        stock.stock_act = stock.stock_act + self.cantidad
        stock.save()
        

        # Llamar al metodo save por defecto de la clase
        super(Movimiento,self).save(*args, **kwargs)

class Foto(models.Model):
    imagen = models.ImageField(upload_to='equipos')
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)

class PrecioRepuesto(models.Model):
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE, related_name='precios')
    proveedor = models.ForeignKey(Proveedor, null=True, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=13, decimal_places=4, blank=True, null=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, blank= True, null=True)
    descripcion_proveedor = models.CharField(max_length = 150, blank= True, null=True)
    modelo_proveedor = models.CharField(max_length=90, null=True, blank=True)
    fabricante = models.CharField(max_length=50, null=True, blank=True)