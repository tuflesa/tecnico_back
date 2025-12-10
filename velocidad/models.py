from estructura.models import Zona
from django.db import models
from estructura.models import Zona
from datetime import datetime
from django.db.models import Min, Max
from django.utils import timezone

class ZonaPerfilVelocidad(models.Model):
    zona = models.OneToOneField(Zona, on_delete=models.CASCADE)
    ip = models.CharField(max_length=20)
    rack = models.IntegerField()
    slot = models.IntegerField()
    db = models.IntegerField()
    dw = models.IntegerField()
    nwords = models.IntegerField(default=4)
    v_max = models.IntegerField(default=100)
    hf_pmax = models.IntegerField(default=700)
    hf_fmax = models.IntegerField(default=400)
    hf_fmin = models.IntegerField(default=200)
    fuerza_max = models.IntegerField(default=100)
    color = models.CharField(max_length=25, blank=True, null=True)
    control_paradas = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.zona.nombre

class Registro(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    velocidad = models.FloatField(null=True, blank=True, default=0)
    potencia = models.FloatField(null=True, blank=True, default=0)
    frecuencia = models.FloatField(null=True, blank=True, default=0)
    presion = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.fecha) + ' - ' + str(self.hora) + ' - ' + self.zona.siglas + ' - ' + str(self.velocidad)  

class TipoParada(models.Model):
    nombre = models.CharField(max_length=12)
    color = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.nombre

class CodigoParada(models.Model):
    nombre = models.CharField(max_length=40)
    tipo = models.ForeignKey(TipoParada, on_delete=models.CASCADE, related_name='codigos')
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name='codigos_parada', null=True, blank=True) # null para codigos validos para todas las máquinas, no null para codigos especificos de una máquina
    siglas = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        if self.zona :
            maquina = self.zona.nombre
        else:
            maquina = 'General'
        return str(self.id) + ' - ' + maquina + ' - ' + self.tipo.nombre + ' - ' + self.nombre

class Parada(models.Model):
    codigo = models.ForeignKey(CodigoParada, on_delete=models.CASCADE, related_name='paradas')
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name='paradas')

    def inicio(self):
        return self.periodos.aggregate(Min('inicio'))['inicio__min']

    def fin(self):
        qs = self.periodos.filter(fin__isnull=True)
        if qs.exists():
            return datetime.now()
        else:
            return self.periodos.aggregate(Max('fin'))['fin__max']

    def duracion(self):
        t=0
        for p in self.periodos.all():
            if p.fin:
                final = p.fin
            else:
                ahora = datetime.now()
                final = timezone.make_aware(ahora, timezone.utc)
            diferencia = final - p.inicio
            t += abs(diferencia.total_seconds())/60 # Minutos
        return t

class Periodo(models.Model):
    parada = models.ForeignKey(Parada, on_delete=models.CASCADE, related_name='periodos')
    inicio = models.DateTimeField(null=True)
    fin = models.DateTimeField(null=True)
    velocidad = models.FloatField(default=0)

class HorarioDia(models.Model):
    fecha = models.DateField(unique=True)
    nombre_dia = models.CharField(max_length=20, default="")
    inicio = models.TimeField(default="06:00")
    fin = models.TimeField(default="22:00")
    es_fin_de_semana = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre_dia} {self.fecha} - {self.inicio}-{self.fin}" 