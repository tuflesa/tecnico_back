from django.db import models
from estructura.models import Zona
from django.utils import timezone
from django import forms
import logging

# Tipo de sección: Formadora, cuchillas, Soldadura, Calibradora, Cabeza de turco
class Tipo_Seccion(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
# Nombre parametros: Nombres de los parametros a emplear según el tipo de plano: Ancho, Diametro exterior, etc ...
class Nombres_Parametros(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
# Tipo de rodillo: Superior, Inferior, Sup/Inf, Lateral 
class Tipo_rodillo(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.nombre
    
# Tipo de plano: Determina los nombres de los parametros a emplear para control de rectificados y para dibujar los rodillos en el Quick Setting
class Tipo_Plano(models.Model):
    nombre = models.CharField(max_length=200)
    tipo_seccion = models.ForeignKey(Tipo_Seccion, on_delete=models.CASCADE, null=True)
    tipo_rodillo = models.ForeignKey(Tipo_rodillo, on_delete=models.CASCADE, null=True)
    croquis = models.ImageField(upload_to='croquis', blank=True, null=True)
    nombres = models.ManyToManyField(Nombres_Parametros, related_name='tipo_plano')

    def __str__(self):
        return self.nombre

# Secciones de una máquina: Formadora, cuchillas, calibradora, etc
class Seccion(models.Model):
    nombre = models.CharField(max_length=50)
    maquina = models.ForeignKey(Zona, on_delete=models.CASCADE)
    pertenece_grupo = models.BooleanField(default=True)
    tipo = models.ForeignKey(Tipo_Seccion, on_delete=models.CASCADE, null=True)
    orden = models.IntegerField(null=True, blank=True) #Solamente se usa para la posición en el tooling chart

    def __str__(self):
        return self.maquina.siglas + '-' + self.nombre

# Operaciones de una sección
class Operacion(models.Model):
    nombre = models.CharField(max_length=50) # Ejemplo: F1
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='operaciones') 
    icono = models.ImageField(upload_to='iconos', blank=True, null=True) 
    orden = models.IntegerField(null=True, blank=True) #Solamente se usa para la posición en el tooling chart

    def __str__(self):
        return self.seccion.maquina.siglas + '-' + self.seccion.nombre + '-' + self.nombre

# Materiales de los que están hechos los rodillos: Ejemplos 1.2379, AMPCO, Ceramica, etc
class Material(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.nombre
    
# Ejes de una operación
class Eje(models.Model):
    operacion = models.ForeignKey(Operacion, on_delete=models.CASCADE, related_name='posiciones')
    tipo = models.ForeignKey(Tipo_rodillo, on_delete=models.CASCADE)
    diametro = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.operacion.seccion.maquina.siglas + '-' + self.operacion.nombre + '-' + self.tipo.nombre

# Bancadas de una sección
class Bancada(models.Model):
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    tubo_madre = models.FloatField(blank=True, null=True)
    dimensiones = models.CharField(max_length=20, blank=True, null=True) # para las dimesiones de una bancada de C.T.

    def nombre(self):
        if self.tubo_madre is not None:
            return f"{self.seccion.nombre}-{self.tubo_madre}"
        else:
            return str(self.seccion.nombre)

# Conjuntos de rodillos de una operación. Son las celdas del Tooling Chart
class Conjunto(models.Model):
    operacion = models.ForeignKey(Operacion, on_delete=models.CASCADE, related_name='conjuntos')
    tubo_madre = models.FloatField(blank=True, null=True)

# Son las celdas del Tooling Chart para las formaciones raras
class Celda (models.Model):
    bancada = models.ForeignKey(Bancada, on_delete=models.CASCADE)
    conjunto = models.ForeignKey(Conjunto, on_delete=models.CASCADE)
    icono = models.ImageField(upload_to='iconos', blank=True, null=True)

# Grupo
class Grupo(models.Model):
    nombre = models.CharField(max_length=50)
    maquina = models.ForeignKey(Zona, on_delete=models.CASCADE)
    tubo_madre = models.FloatField(blank=True, null=True)
    bancadas = models.ManyToManyField(Bancada, blank=True, related_name='grupos')

    def __str__(self) -> str:
        return self.nombre

# Forma
class Forma(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.nombre

# Rodillos
class Rodillo(models.Model):
    nombre = models.CharField(max_length=50)
    operacion = models.ForeignKey(Operacion, on_delete=models.CASCADE, related_name='rodillos')
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.ForeignKey(Tipo_rodillo, on_delete=models.CASCADE)
    tipo_plano = models.ForeignKey(Tipo_Plano, on_delete=models.CASCADE, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    diametro = models.FloatField(blank=True, null=True)
    forma = models.ForeignKey(Forma, on_delete=models.CASCADE, null=True, blank=True)
    descripcion_perfil = models.CharField(max_length=50, null=True, blank=True)
    dimension_perfil = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self) -> str:
        return self.nombre

# Parámetros estándar: Parametros de un rodillo según plano sin rectificar. Al crear una revisión de un plano, se deben actualizar.
class Parametros_Estandar(models.Model):
    nombre = models.CharField(max_length=50)
    valor = models.FloatField()
    rodillo = models.ForeignKey(Rodillo, on_delete=models.CASCADE)

# Elementos de un conjunto de rodillos. Que rodillo en que posición dentro de un conjunto de rodillos
class Elemento(models.Model):
    conjunto = models.ForeignKey(Conjunto, on_delete=models.CASCADE, related_name='elementos')
    eje = models.ForeignKey(Eje, on_delete=models.CASCADE)
    rodillo = models.ForeignKey(Rodillo, on_delete=models.CASCADE)

# Montaje
class Montaje(models.Model):
    nombre = models.CharField(max_length=50)
    maquina = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name='montajes')
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    bancadas = models.ForeignKey(Bancada, on_delete=models.CASCADE, null=True, blank=True, default=None) #es la bancada de CT + grupo = montaje

    def __str__(self) -> str:
        return self.nombre

# Planos de los rodillos
class Plano(models.Model):
    nombre = models.CharField(max_length=200, null=True, blank=True, default=None)
    rodillos = models.ManyToManyField(Rodillo, related_name='planos')

    #si lo activo no funciona la acción de guardar, hay que revisar el código.
    """ def save(self, *args, **kwargs):
        super(Plano, self).save(*args, **kwargs)  # Guarda primero para tener un ID

        if self.nombre is None and self.rodillos.exists() and self.id:
            print("estamos dentro del if")
            maquina = self.rodillos[0]
            seccion = self.rodillos.firt().operacion.seccion.nombre
            num = self.id  # Ahora hay un ID disponible
            self.nombre = f"adios_{maquina}_{seccion}_{num}"
            print("datos maquina y seccion")
            print(maquina)
            print(seccion)
            self.save(update_fields=['nombre'])  # Guarda solo el campo 'nombre' """

   
# Revisión: Modificaciones de un plano  
class Revision(models.Model):
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE, blank=False, null=False)
    motivo = models.TextField(max_length=250, blank=False, null=False)
    archivo = models.FileField(upload_to='planos', blank=False, null=False)
    fecha = models.DateField(default=timezone.now)

#Instancia: Un rodillo en concreto
class Instancia(models.Model):
    nombre = models.CharField(max_length=200)
    rodillo = models.ForeignKey(Rodillo, on_delete=models.CASCADE)
    planos = models.ManyToManyField(Plano, related_name='instancias')

# Parámetros: Parametros de un rodillo según plano sin rectificar. Al crear una revisión de un plano, se deben actualizar.
class Parametros(models.Model):
    nombre = models.CharField(max_length=50)
    valor = models.FloatField()
    revision = models.ForeignKey(Revision, on_delete=models.CASCADE)