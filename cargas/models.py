from django.db import models
from django.db.models.fields import CharField
from django.utils import timezone
from datetime import date
from estructura.models import Empresa

class Agencia(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    contacto = models.CharField(max_length=120, blank=True, null=True)
    observaciones = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Bascula(models.Model):
    nombre = CharField(max_length=50)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    url = CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nombre
class Estados(models.Model):
    nombre_estado = models.CharField(max_length=12)
    def __str__(self):
            return self.nombre_estado
class Situacion(models.Model):
    nombre_situacion = models.CharField(max_length=30)
    color = models.CharField(max_length=10)
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE, blank=True, null=True)

class Tipo_carga(models.Model):
    tipo = models.CharField(max_length=10)
    requiere_albaran_agencia = models.BooleanField(default=False)

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
    puerta = models.IntegerField(null=True, blank=True)
    observaciones = models.CharField(max_length=300, null=True, blank=True)
    fecha_prevista = models.DateField(default=timezone.now)
    cliente = models.CharField(max_length=50, default="none")
    situacion = models.ForeignKey(Situacion, on_delete=models.CASCADE, null=True, blank=True) #cambiar por default=1
    tipo_carga = models.ForeignKey(Tipo_carga, on_delete=models.CASCADE, null=True, blank=True) #quitar null y blank
    documentacion_entregada = models.BooleanField(default=False)
    albaran_agencia = models.BooleanField(default=False)
    archivo = models.FileField(upload_to='hoja_carga', blank=True, null=True )

class Llamada(models.Model):
    carga = models.ForeignKey(Carga, on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today)
    hora = models.TimeField(auto_now_add=True)
    puerta = models.IntegerField()