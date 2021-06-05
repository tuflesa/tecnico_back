from estructura.models import Zona
from django.db import models
from estructura.models import Zona

class ZonaPerfilVelocidad(models.Model):
    zona = models.OneToOneField(Zona, on_delete=models.CASCADE)
    ip = models.CharField(max_length=20)
    rack = models.IntegerField()
    slot = models.IntegerField()
    db = models.IntegerField()
    dw = models.IntegerField()
    color = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self) -> str:
        return self.zona.nombre

class Registro(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    velocidad = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.fecha) + ' - ' + str(self.hora) + ' - ' + self.zona.siglas + ' - ' + str(self.velocidad)  
