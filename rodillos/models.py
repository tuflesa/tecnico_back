from django.db import models
from estructura.models import Zona, Empresa
from repuestos.models import Proveedor
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
from .storages import OverwriteStorage
import logging
import datetime

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
    siglas = models.CharField(max_length=10, blank=True, null=True) 

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

class Icono(models.Model):
    nombre = models.CharField(max_length=20)
    icono = models.ImageField(upload_to='iconos', blank=True, null=True) 
    def __str__(self) -> str:
        return self.nombre

# Operaciones de una sección
class Operacion(models.Model):
    nombre = models.CharField(max_length=50) # Ejemplo: F1
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='operaciones') 
    icono = models.ForeignKey(Icono,  on_delete=models.CASCADE, blank=True, null=True)
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
    numero_ejes = models.IntegerField(default=1)

    def __str__(self):
        return self.operacion.seccion.maquina.siglas + '-' + self.operacion.nombre + '-' + self.tipo.nombre

# Bancadas de una sección
class Bancada(models.Model):
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    tubo_madre = models.FloatField(blank=True, null=True)
    dimensiones = models.CharField(max_length=20, blank=True, null=True) # para las dimesiones de una bancada de C.T.
    espesores = models.CharField(max_length=20, default='0÷0')
    nombre_grupo = models.CharField(max_length=50, blank=True, null=True)

    def nombre(self):
        if self.tubo_madre is not None:
            return f"{self.seccion.nombre}-{self.tubo_madre}"
        else:
            return str(self.seccion.nombre)

# Conjuntos de rodillos de una operación. Son las celdas del Tooling Chart
class Conjunto(models.Model):
    operacion = models.ForeignKey(Operacion, on_delete=models.CASCADE, related_name='conjuntos')
    tubo_madre = models.FloatField(blank=True, null=True)
    espesores = models.CharField(max_length=20, blank=True, null=True)
    

# Son las celdas del Tooling Chart para las formaciones raras
class Celda (models.Model):
    bancada = models.ForeignKey(Bancada, on_delete=models.CASCADE, related_name='celdas')
    conjunto = models.ForeignKey(Conjunto, on_delete=models.CASCADE)
    icono = models.ImageField(upload_to='iconos', blank=True, null=True)
    operacion = models.ForeignKey(Operacion, on_delete=models.CASCADE, blank=True, null=True)

# Grupo
class Grupo(models.Model):
    nombre = models.CharField(max_length=50)
    maquina = models.ForeignKey(Zona, on_delete=models.CASCADE)
    tubo_madre = models.FloatField(blank=True, null=True)
    bancadas = models.ManyToManyField(Bancada, blank=True, related_name='grupos')
    espesor_1 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    espesor_2 = models.DecimalField(max_digits=5, decimal_places=2, default=0)

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
    tipo_plano = models.ForeignKey(Tipo_Plano, on_delete=models.CASCADE, null=True, blank=True)
    diametro = models.FloatField(blank=True, null=True)
    forma = models.ForeignKey(Forma, on_delete=models.CASCADE, null=True, blank=True)
    descripcion_perfil = models.CharField(max_length=50, null=True, blank=True)
    dimension_perfil = models.CharField(max_length=3, null=True, blank=True)
    espesor_1 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    espesor_2 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    espesor = models.BooleanField(default=False)
    num_instancias = models.IntegerField(default=0,blank=True, null=True)
    num_ejes = models.IntegerField(default=1,blank=True, null=True)
    archivo = models.FileField(upload_to='programa', blank=True, null=True)

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
    anotciones_montaje = models.CharField(max_length=100, null=True, blank=True)

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
    cod_antiguo = models.CharField(max_length=200, null=True, blank=True, default=None)
    descripcion = models.CharField(max_length=200, null=True, blank=True, default=None)
    xa_rectificado = models.BooleanField(default=False)
   
# Revisión: Modificaciones de un plano  
class Revision(models.Model):
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE, blank=False, null=False)
    motivo = models.TextField(max_length=250, blank=False, null=False)
    archivo = models.FileField(upload_to='planos', blank=False, null=False)
    fecha = models.DateField(default=timezone.now)
    nombre = models.CharField(max_length=200, null=True, blank=True, default=None)

# Posicones de una instancia: Operador, Motor, None
class Posicion(models.Model):
    nombre = models.CharField(max_length=50, null=True, blank=True)
    siglas = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.nombre

#Instancia: Un rodillo en concreto
class Instancia(models.Model):
    nombre = models.CharField(max_length=200)
    rodillo = models.ForeignKey(Rodillo, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, blank=True, null=True)
    especial = models.BooleanField(default=False, null=True, blank=True)
    diametro = models.FloatField(null=True, blank=True) # diametro de fondo
    diametro_ext = models.FloatField(null=True, blank=True)
    ancho = models.FloatField(null=True, blank=True)
    activa_qs = models.BooleanField(default=True, null=True, blank=True)
    obsoleta = models.BooleanField(default=False, null=True, blank=True)
    diametro_centro = models.FloatField(null=True, blank=True)
    posicion = models.ForeignKey(Posicion, blank=True, null=True, on_delete=models.SET_NULL)

# Parámetros: Parametros de un rodillo según plano sin rectificar. Al crear una revisión de un plano, se deben actualizar.
class Parametros(models.Model):
    nombre = models.CharField(max_length=50)
    valor = models.FloatField()
    revision = models.ForeignKey(Revision, on_delete=models.CASCADE)

class ContadorRectificaciones(models.Model):
    year = models.IntegerField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    contador = models.IntegerField(default=0)

    def __str__(self):
        return str(self.year) + '-' + str(self.contador)

class Rectificacion(models.Model):
    numero = models.CharField(max_length=20, null=True, blank=True, default=None)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField(default=timezone.now)
    fecha_estimada = models.DateField(default=timezone.now)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Zona, on_delete=models.CASCADE)
    finalizado = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        # Generar nuevo número si el campo numero es None (null)
        if self.numero is None:
            currentDateTime = datetime.datetime.now()
            date = currentDateTime.date()
            year = date.strftime("%Y")

            contador = ContadorRectificaciones.objects.filter(year=year, empresa=self.empresa)
            if (len(contador)==0):
                contador = ContadorRectificaciones(year=year, contador=0, empresa=self.empresa)
                contador.save()
                numero=1
            else:
                contador = ContadorRectificaciones.objects.get(year=year, empresa=self.empresa)
                numero=contador.contador+1

            contador.contador = numero
            contador.save()

            self.numero = self.empresa.siglas + '-' + year + '-R-' + str(numero).zfill(3)
        # Llamar al metodo save por defecto de la clase
        super(Rectificacion,self).save(*args, **kwargs)

class LineaRectificacion(models.Model):
    TIPO_RECTIFICADO_CHOICES = [
        ('estandar', 'Estándar'),
        ('axial', 'Axial'),
    ]
    rectificado = models.ForeignKey(Rectificacion, on_delete=models.CASCADE)
    instancia = models.ForeignKey(Instancia, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField(default=timezone.now)
    diametro = models.FloatField(null=True, blank=True)
    diametro_ext = models.FloatField(null=True, blank=True)
    ancho = models.FloatField(null=True, blank=True)
    diametro_centro = models.FloatField(null=True, blank=True)
    nuevo_diametro = models.FloatField(null=True, blank=True)
    nuevo_diametro_ext = models.FloatField(null=True, blank=True)
    nuevo_ancho = models.FloatField(null=True, blank=True)
    nuevo_diametro_centro = models.FloatField(null=True, blank=True)
    rectificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_rectificado = models.DateField(blank=True, null=True)
    tipo_rectificado = models.CharField(max_length=10, choices=TIPO_RECTIFICADO_CHOICES, default='estandar')
    finalizado = models.BooleanField(default=False)
    archivo = models.FileField(upload_to='programa', blank=True, null=True, storage=OverwriteStorage())
    observaciones = models.CharField(max_length=600, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, null=True, blank=True, on_delete=models.CASCADE)