from django.db import models
from estructura.models import Zona

class Forma(models.Model):
    codigo_forma = models.CharField(max_length=1, primary_key=True)
    descripcion = models.CharField(max_length=15)
    abreviatura = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.codigo_forma} - {self.descripcion}"

class Acumulador(models.Model):
    nombre = models.CharField(max_length=50)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    maquina_siglas = models.CharField(max_length=4, null=True, blank=True)
    maquila_siglas = models.CharField(max_length=4, null=True, blank=True)
    of_activa = models.CharField(max_length=8, null=True, blank=True)
    n_bobina_activa = models.IntegerField(null=True, blank=True)
    n_bobina_ultima = models.IntegerField(null=True, blank=True)
    ip = models.CharField(max_length=20, null=True, blank=True)
    rack = models.IntegerField(null=True, blank=True)
    slot = models.IntegerField(null=True, blank=True)
    db = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class OF(models.Model):
    numero = models.CharField(max_length=8)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, null=True)
    inicio = models.DateTimeField()
    fin = models.DateTimeField(null=True, blank=True)
    grupo = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return self.numero

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
    orden = models.ForeignKey(OF, on_delete=models.SET_NULL, null=True, blank=True, related_name='flejes')

    def ancho(self):
        return int(self.IdArticulo[6:-3])
    
    def espesor(self):
        return float(self.IdArticulo[9:])/10.0
    
    def calidadSTR(self):
        array = self.descripcion.split()
        return array[1]
    
    def metros_teorico(self):
        metros = (self.peso *1000) / (self.espesor() * self.ancho() * 7.85)
        return metros
    
    def metros_tubo(self):
        metros = 0
        for tubo in self.tubos.all():
            metros += tubo.n_tubos * tubo.largo/1000
        return metros
    
    def __str__(self):
        return str(self.pos) + ' - ' + self.descripcion

class Tubos(models.Model):
    n_tubos = models.IntegerField(default=0)
    largo = models.FloatField()
    fleje = models.ForeignKey(Flejes, on_delete=models.CASCADE, related_name='tubos')
    dim1 = models.FloatField(null=True, blank=True) # 0 si el tubo es redondo, ancho en cuadrado o rectangular
    dim2 = models.FloatField(null=True, blank=True) # diametro si es redondo, alto si es cuadrado o rectangular
    fecha_entrada = models.DateTimeField(blank=True, null=True)
    fecha_salida = models.DateTimeField(blank=True, null=True)

    def descripcion(self):
        if (self.dim2):
            if self.dim1 == 0: #Tubo redondo
                tipo_tubo = 'Red. ' + f"{self.dim2:.1f}"
            else: # Tubo cuadrado o rectangular
                if (self.dim1 == self.dim2): # Cuadrado
                    tipo_tubo = 'Cuad. ' + f"{self.dim1:.1f}" + 'x' + f"{self.dim2:.1f}"
                else:
                    tipo_tubo = 'Rect. ' + f"{self.dim1:.1f}" + 'x' + f"{self.dim2:.1f}"

            return tipo_tubo + 'x' + str(self.fleje.espesor()) + ' - ' + self.fleje.calidadSTR()  + ' x ' + f"{self.largo:.0f}"
        else:
            return 'Tubo sin dimensiones'
    
    def __str__(self):
        return self.descripcion()
