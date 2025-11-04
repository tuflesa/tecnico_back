from xmlrpc.client import boolean
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
#from django.db.models.deletion import CASCADE
from estructura.models import Empresa, Equipo, Seccion, Zona
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class ContadorNotificaciones(models.Model):
    year = models.IntegerField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    contador = models.IntegerField(default=0)

    def __str__(self):
        return str(self.year) + '-' + str(self.contador)

class Notificacion(models.Model): # Notificación 5W+2H Plus
    # 5W+2H
    que = models.TextField(max_length=750) # What. Que sucede
    cuando = models.TextField(max_length=150) # When. Cuando sucede, en que momento del día
    donde = models.TextField(max_length=150) # Where. Donde está el problema
    quien = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='notificaciones_enviadas') # Who. Quien informa del problema
    como = models.TextField(max_length=250) # How. Como se distingue del estado normal
    cuanto = models.TextField(max_length=150) # How many. Cuantas veces ocurre el problema: Una vez al día, continuamente, ...
    porque = models.TextField(max_length=250) # Why. Por que cree que ocurre el problema.
    # Plus
    numero = models.CharField(max_length=16, null=True, blank=True, default=None)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, blank=True, null=True, related_name='notificaciones_creadas')
    fecha_creacion = models.DateField(default=timezone.now)
    #para = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='notificaciones_recividas') # A quien se informa del problema
    revisado = models.BooleanField(default=False)
    descartado = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=False)
    conclusion = models.TextField(max_length=800, blank=True, null=True) # Explicación de si queda resuelto o motivos por los que se descarta
    peligrosidad = models.BooleanField(default=False)
    seguridad = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Generar nuevo número si el campo numero es None (null)
        if self.numero is None:
            currentDateTime = datetime.datetime.now()
            date = currentDateTime.date()
            year = date.strftime("%Y")

            contador = ContadorNotificaciones.objects.filter(year=year, empresa=self.empresa)
            if (len(contador)==0):
                contador = ContadorNotificaciones(year=year, contador=0, empresa=self.empresa)
                contador.save()
                numero=1
            else:
                contador = ContadorNotificaciones.objects.get(year=year, empresa=self.empresa)
                numero=contador.contador+1

            contador.contador = numero
            contador.save()

            self.numero = self.empresa.siglas + '-' + year + '-N-' + str(numero).zfill(3)
        # Llamar al metodo save por defecto de la clase
        super(Notificacion,self).save(*args, **kwargs)
        
    def __str__(self):
        return self.que

class Especialidad(models.Model): # Electricidad, Electronica, Mecanica, Fontanería ...
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# El tipo de tarea vale para Tarea y para Partes de trabajo
class TipoTarea(models.Model): # Correctiva, Preventiva, Mejora, PRL ...
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class TipoPeriodo(models.Model): # Anual, Mensual, Semanal ... 
    nombre = models.CharField(max_length=50)
    cantidad_dias = models.IntegerField(default=1)

    def __str__(self):
        return self.nombre

class Tarea(models.Model): 
    nombre = models.CharField(max_length=150)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)    
    prioridad = models.IntegerField(default=50) # Número de 0 a 100. 100 máxima prioridad
    #trabajo = models.TextField(blank=True, null=True) #trabajo a realizar, detalles
    observaciones = models.TextField(blank=True, null=True)
    observaciones_trab = models.TextField(blank=True, null=True) #no guarda información??
    tipo_periodo = models.ForeignKey(TipoPeriodo, on_delete=models.CASCADE, null=True, blank=True)
    periodo = models.IntegerField(default=0)

    """ def equipo_nombre(self):
        return self.equipo.nombre """

    def especialidad_nombre(self):
        return self.especialidad.nombre
    
    def __str__(self):
        return self.nombre

class EstadoLineasTareas(models.Model): # Planificadas, En Ejecución, Finalizadas ... 
    nombre = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre

class ContadorPartes(models.Model):
    year = models.IntegerField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    contador_parte = models.IntegerField(default=0)

    def __str__(self):
        return str(self.year) + '-' + str(self.contador_parte)

class ParteTrabajo(models.Model):
    nombre = models.CharField(max_length=150)
    #notificacion = models.ForeignKey(Notificacion, on_delete=models.CASCADE, null=True, blank=True, related_name='partes')
    tipo = models.ForeignKey(TipoTarea, on_delete=models.CASCADE)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    #responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='partes_responsable')
    finalizado = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateField(default=timezone.now)
    fecha_prevista_inicio = models.DateField(blank=True, null=True)
    fecha_finalizacion = models.DateField(blank=True, null=True)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, blank=True, null=True, related_name='partes_creados')
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, blank=True, related_name='partes_creados')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, blank=True, null=True, related_name='partes_creados')
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, blank=True,related_name='partes_creados')
    tarea = models.ManyToManyField(Tarea, blank=True, related_name='partes')
    estado = models.ForeignKey(EstadoLineasTareas, on_delete=models.SET_NULL, blank=True, null=True)
    num_parte = models.CharField(max_length=16, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        # Generar nuevo número si el campo num_parte es None (null)
        if self.num_parte is None:
            currentDateTime = datetime.datetime.now()
            date = currentDateTime.date()
            year = date.strftime("%Y")

            contador_parte = ContadorPartes.objects.filter(year=year, empresa=self.empresa)
            if (len(contador_parte)==0):
                contador_parte = ContadorPartes(year=year, contador_parte=0, empresa=self.empresa)
                contador_parte.save()
                num_parte=1
            else:
                contador_parte = ContadorPartes.objects.get(year=year, empresa=self.empresa)
                num_parte=contador_parte.contador_parte+1

            contador_parte.contador_parte = num_parte
            contador_parte.save()

            self.num_parte = self.empresa.siglas + '-' + year + '-P-' + str(num_parte).zfill(3)
        # Llamar al metodo save por defecto de la clase
        super(ParteTrabajo,self).save(*args, **kwargs)

    """ def finalizado(self):
        fin = True
        for linea in self.lineas:
            if linea.fecha_fin is None:
                fin = False
                break
        return fin """

    """ def fecha_fin(self):
        fecha = None
        if not self.finalizado:
            return fecha
        for linea in self.lineas:
            if fecha < linea.fecha_fin:
                fecha = linea.fecha_fin
        return fecha """
    
    """ def equipo_nombre(self):
        return self.equipo.nombre """

    def tipo_nombre(self):
        return self.tipo.nombre  

    def estado_nombre(self):
        return self.estado.nombre 
    
    """ def creado_nombre(self):
        return self.creada_por.get_full_name()  """

    def __str__(self):
        return self.nombre

class LineaParteTrabajo(models.Model):
    parte = models.ForeignKey(ParteTrabajo, on_delete=models.CASCADE, related_name='lineas')
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    fecha_plan = models.DateField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.ForeignKey(EstadoLineasTareas, on_delete=models.SET_NULL, blank=True, null=True)
    observaciones_trab = models.TextField(blank=True, null=True)
    #responsables = models.ManyToManyField(User, related_name='lineas_parte_trabajo')

    def __str__(self):
        return self.tarea.nombre

class GastosParte(models.Model):
    parte = models.ForeignKey(ParteTrabajo, on_delete=models.CASCADE, related_name='gastos')
    linea = models.ForeignKey(LineaParteTrabajo, on_delete=models.CASCADE, related_name='gastos', blank=True, null=True)
    descripcion = models.CharField(max_length=150)
    cantidad = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=13, decimal_places=4, blank=True, null=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, blank= True, null=True, default=0)
    total = models.DecimalField(max_digits=13, decimal_places=4, blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 

class TrabajadoresLineaParte(models.Model):
    linea = models.ForeignKey(LineaParteTrabajo, on_delete=models.CASCADE, related_name='lineas')
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    trabajador = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

class Reclamo(models.Model):
    notificacion = models.ForeignKey(Notificacion, on_delete=models.CASCADE, related_name='notificaciones')
    fecha = models.DateField(blank=True, null=True)
    trabajador = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.notificacion.numero

