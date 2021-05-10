from django.db import models
from django.utils import timezone
from estructura.models import Empresa

class Agencia(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    contacto = models.CharField(max_length=120, blank=True, null=True)
    observaciones = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Carga(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, blank=True, null=True)
    remolque = models.CharField(max_length=20)
    agencia = models.ForeignKey(Agencia, on_delete=models.CASCADE, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_entrada = models.DateField(default=timezone.now)
    hora_entrada = models.TimeField(default=timezone.now)
    tara = models.IntegerField()
    destino = models.CharField(max_length=50, null=True, blank=True)
    bruto = models.IntegerField(null=True, blank=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
