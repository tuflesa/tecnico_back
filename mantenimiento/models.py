from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from estructura.models import Empresa, Equipo
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
    que = models.TextField(max_length=250) # What. Que sucede
    cuando = models.TextField(max_length=150) # When. Cuando sucede, en que momento del día
    donde = models.TextField(max_length=150) # Where. Donde está el problema
    quien = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='notificaciones_enviadas') # Who. Quien informa del problema
    como = models.TextField(max_length=250) # How. Como se distingue del estado normal
    cuanto = models.TextField(max_length=150) # How many. Cuantas veces ocurre el problema: Una vez al día, continuamente, ...
    porque = models.TextField(max_length=250) # Why. Por que cree que ocurre el problema.
    # Plus
    numero = models.CharField(max_length=16, null=True, blank=True, default=None)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(default=timezone.now)
    para = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='notificaciones_recividas') # A quien se informa del problema
    revisado = models.BooleanField(default=False)
    descartado = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=False)
    conclusion = models.TextField(max_length=250, blank=True, null=True) # Explicación de si queda resuelto o motivos por los que se descarta

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

    # def abierto(self):
    #     cerrado = False
    #     if self.descartado:
    #         return cerrado
    #     # Si todos los partes de esta notificación están cerrados False sino True
    #     for parte in self.partes:
    #         if not parte.finalizado:
    #             break
    #     return not cerrado
        
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

    def __str__(self):
        return self.nombre

class Tarea(models.Model): 
    nombre = models.CharField(max_length=150)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoTarea, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    tipo_periodo = models.ForeignKey(TipoPeriodo, on_delete=models.CASCADE)
    periodo = models.IntegerField()
    prioridad = models.IntegerField(default=50) # Número de 0 a 100. 100 máxima prioridad
    observaciones = models.TextField()

    def __str__(self):
        return self.nombre

class ParteTrabajo(models.Model):
    nombre = models.CharField(max_length=150)
    notificacion = models.ForeignKey(Notificacion, on_delete=models.CASCADE, null=True, blank=True, related_name='partes')
    tipo = models.ForeignKey(TipoTarea, on_delete=models.CASCADE)
    creada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='partes_creados')
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='partes_responsable')
    # finalizado = models.BooleanField(default=False)
    observaciones = models.TextField()

    def finalizado(self):
        fin = True
        for linea in self.lineas:
            if linea.fecha_fin is None:
                fin = False
                break
        return fin

    def fecha_fin(self):
        fecha = None
        if not self.finalizado:
            return fecha
        for linea in self.lineas:
            if fecha < linea.fecha_fin:
                fecha = linea.fecha_fin
        return fecha

    def __str__(self):
        return self.nombre

class LineaParteTrabajo(models.Model):
    parte = models.ForeignKey(ParteTrabajo, on_delete=models.CASCADE, related_name='lineas')
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    responsables = models.ManyToManyField(User, related_name='lineas_parte_trabajo')

    def __str__(self):
        return self.tarea.nombre



