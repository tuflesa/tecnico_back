from django.db import models
from estructura.models import Zona

class Acumulador(models.Model):
    nombre = models.CharField(max_length=50)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    maquina_siglas = models.CharField(max_length=4, null=True, blank=True)
    of_activa = models.CharField(max_length=8, null=True, blank=True)
    n_bobina_activa = models.IntegerField(null=True, blank=True)
    n_bobina_ultima = models.IntegerField(null=True, blank=True)
    ip = models.CharField(max_length=20, null=True, blank=True)
    rack = models.IntegerField(null=True, blank=True)
    slot = models.IntegerField(null=True, blank=True)
    db = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre

# Registra todos los flejes que entran en los acumuladores    
class Flejes(models.Model):
    pos = models.IntegerField()
    idProduccion = models.CharField(max_length=10)
    IdArticulo = models.CharField(max_length=12)
    peso = models.IntegerField()
    of = models.CharField(max_length=8)
    maquina_siglas = models.CharField(max_length=4)
    descripcion = models.CharField(max_length=50)
    acumulador = models.ForeignKey(Acumulador, on_delete=models.CASCADE, related_name='flejes')
    metros_medido = models.FloatField(default=0)
    fecha_entrada = models.DateField(blank=True, null=True)
    hora_entrada = models.TimeField(blank=True, null=True)
    fecha_salida = models.DateField(blank=True, null=True)
    hora_salida = models.TimeField(blank=True, null=True)
    finalizada = models.BooleanField(default=False)

    def ancho(self):
        return int(self.IdArticulo[6:-3])
    
    def espesor(self):
        return float(self.IdArticulo[9:])/10.0
    
    def metros_teorico(self):
        metros = (self.peso *1000) / (self.espesor() * self.ancho() * 7.85)
        return metros
    
    def metros_tubo(self):
        metros = 0
        for tubo in self.tubos.all():
            metros += tubo.n_tubos * tubo.largo/1000
        return metros

class Tubos(models.Model):
    n_tubos = models.IntegerField(default=0)
    largo = models.FloatField()
    fleje = models.ForeignKey(Flejes, on_delete=models.CASCADE, related_name='tubos')
