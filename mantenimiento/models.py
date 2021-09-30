from django.db import models
from django.db.models.base import Model
from estructura.models import Equipo
from django.contrib.auth.models import User

class Notificacion(models.Model): # Notificación 5W+2H
    que = models.TextField(max_length=250) # What. Que sucede
    cuando = models.TextField(max_length=150) # When. Cuando sucede, en que momento del día
    donde = models.TextField(max_length=150) # Where. Donde está el problema
    quien = models.ForeignKey(User) # Who. Quien informa del problema
    como = models.TextField(max_length=250) # How. Como se distingue del estado normal
    cuanto = models.TextField(max_length=150) # How many. Cuantas veces ocurre el problema: Una vez al día, continuamente, ...
    porque = models.TextField(max_length=250) # Why. Por que cree que ocurre el problema.


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
    prioridad = periodo = models.IntegerField(default=50) # Número de 0 a 100. 100 máxima prioridad
    observaciones = models.TextField()

    def __str__(self):
        return self.nombre

class ParteTrabajo(models.Model):
    nombre = models.CharField(max_length=150)
    tipo = models.ForeignKey(TipoTarea, on_delete=models.CASCADE)
    creada_por = models.ForeignKey(User)
    responsable = models.ForeignKey(User)
    finalizado = models.BooleanField(default=False)
    observaciones = models.TextField()

    def __str__(self):
        return self.nombre

class LineaParteTrabajo(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    responsable = models.ForeignKey(User)

    def __str__(self):
        return self.tarea.nombre


