from estructura.models import Zona
from django.db import models
from datetime import datetime
from django.db.models import Min, Max
from django.utils import timezone
from django.contrib.auth.models import User

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
    
class Turnos(models.Model): # Escritura, lectura, edicion....
    turno = models.CharField(max_length=1)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name='turnos', null=True, blank=True)
    maquinista = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.turno} - {self.maquinista}" 

class TipoParada(models.Model):
    nombre = models.CharField(max_length=12)
    color = models.CharField(max_length=15, null=True)
    para_informar = models.BooleanField(default=False)
    siglas = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class PalabrasClave(models.Model):
    nombre = models.CharField(max_length=40)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, null=True, blank=True) # null para codigos validos para todas las máquinas, no null para codigos especificos de una máquina

    def __str__(self):
        return self.nombre

class CodigoParada(models.Model):
    nombre = models.CharField(max_length=40)
    tipo = models.ForeignKey(TipoParada, on_delete=models.CASCADE, related_name='codigos')
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name='codigos_parada', null=True, blank=True) # null para codigos validos para todas las máquinas, no null para codigos especificos de una máquina
    siglas = models.CharField(max_length=10, blank=True, null=True)
    palabra_clave = models.ForeignKey(PalabrasClave, on_delete=models.CASCADE, null=True, blank=True, related_name='codigos')
    codigoProdDB = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        if self.zona :
            maquina = self.zona.nombre
        else:
            maquina = 'General'
        if self.palabra_clave:
            pc = self.palabra_clave.nombre
        else:
            pc = ''
        return str(self.id) + ' - ' + maquina + ' - ' + self.tipo.nombre + ' - ' + self.nombre + ' - ' + pc

class Parada(models.Model):
    codigo = models.ForeignKey(CodigoParada, on_delete=models.CASCADE, related_name='paradas')
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name='paradas')
    observaciones = models.CharField(max_length=500, blank=True, null=True)
    of = models.CharField(max_length=8, null=True, blank=True)
    pos = models.CharField(max_length=3, null=True, blank=True)

    def inicio(self):
        return self.periodos.aggregate(Min('inicio'))['inicio__min']
    
    # def fin(self):
    #     qs = self.periodos.filter(fin__isnull=True)
    #     if qs.exists():
    #         return timezone.now()  # aware en UTC
    #     else:
    #         return self.periodos.aggregate(Max('fin'))['fin__max']


    def fin(self):
        qs = self.periodos.filter(fin__isnull=True)
        if qs.exists():
            return datetime.now()
        else:
            return self.periodos.aggregate(Max('fin'))['fin__max']
        
    # def duracion(self):
    #     t = 0
    #     for p in self.periodos.all():
    #         if p.fin:
    #             final = p.fin
    #         else:
    #             final = timezone.now()  # aware en UTC

    #         diferencia = final - p.inicio
    #         t += abs(diferencia.total_seconds()) / 60
    #     return t

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
    turno = models.ForeignKey(Turnos, on_delete=models.SET_NULL, null=True, blank=True)
    
class HorarioDia(models.Model):
    fecha = models.DateField()
    nombre_dia = models.CharField(max_length=20, default="")
    inicio = models.TimeField(default="06:00")
    fin = models.TimeField(default="22:00")
    es_festivo = models.BooleanField(default=False) # o vacaciones = es_no_laborable
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name='horarios', null=True, blank=True)
    turno_mañana = models.ForeignKey(Turnos, on_delete=models.CASCADE, related_name='horario_mañana', null=True, blank=True)
    turno_tarde = models.ForeignKey(Turnos, on_delete=models.CASCADE, related_name='horario_tarde', null=True, blank=True)
    turno_noche = models.ForeignKey(Turnos, on_delete=models.CASCADE, related_name='horario_noche', null=True, blank=True)
    cambio_turno_1 = models.TimeField(default="14:00")
    cambio_turno_2 = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('fecha', 'zona')

    def semana(self):
        return self.fecha.isocalendar().week

    def __str__(self):
        return f"{self.nombre_dia} {self.fecha} - {self.inicio}-{self.fin}" 

class DestrezasVelocidad(models.Model): # Escritura, lectura, edicion....
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre