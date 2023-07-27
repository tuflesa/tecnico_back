from django.db import models
from estructura.models import Zona

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
    
# Tipo de plano: Determina los nombres de los parametros a emplear para control de rectificados y para dibujar los rodillos en el Quick Setting
class Tipo_Plano(models.Model):
    nombre = models.CharField(max_length=200)
    tipo_seccion = models.ForeignKey(Tipo_Seccion, on_delete=models.CASCADE, null=True)
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

    def __str__(self):
        return self.maquina.siglas + '-' + self.nombre

# Operaciones de una sección
class Operacion(models.Model):
    nombre = models.CharField(max_length=50) # Ejemplo: F1
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='operaciones') 
    icono = models.ImageField(upload_to='iconos', blank=True, null=True) 

    def __str__(self):
        return self.seccion.maquina.siglas + '-' + self.seccion.nombre + '-' + self.nombre

# Materiales de los que están hechos los rodillos: Ejemplos 1.2379, AMPCO, Ceramica, etc
class Material(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.nombre

# Tipo de rodillo: Superior, Inferior, Sup/Inf, Lateral 
class Tipo_rodillo(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.nombre
    
# Ejes de una operación
class Eje(models.Model):
    nombre = models.CharField(max_length=50) # Ejemplos: superior, inferior, lateral, ...
    operacion = models.ForeignKey(Operacion, on_delete=models.CASCADE, related_name='posiciones')
    tipo = models.ForeignKey(Tipo_rodillo, on_delete=models.CASCADE)
    diametro = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.operacion.seccion.maquina.siglas + '-' + self.operacion.seccion.nombre + '-' +   self.operacion.nombre + ' - ' + self.nombre

# Grupo
class Grupo(models.Model):
    nombre = models.CharField(max_length=50)
    maquina = models.ForeignKey(Zona, on_delete=models.CASCADE)
    tubo_madre = models.FloatField(blank=True, null=True)

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

    def __str__(self) -> str:
        return self.nombre

# Parámetros estándar: Parametros de un rodillo según plano sin rectificar. Al crear una revisión de un plano, se deben actualizar.
class Parametros_Estandar(models.Model):
    nombre = models.CharField(max_length=50)
    valor = models.FloatField()
    rodillo = models.ForeignKey(Rodillo, on_delete=models.CASCADE)

# Bancadas de una sección
class Bancada(models.Model):
    nombre = models.CharField(max_length=50)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    grupos = models.ManyToManyField(Grupo,related_name='bancadas')

    def __str__(self) -> str:
        return self.nombre

# Conjuntos de rodillos de una operación. Son las celdas del Tooling Chart
class Conjunto(models.Model):
    nombre = models.CharField(max_length=50)
    bancada = models.ForeignKey(Bancada, on_delete=models.CASCADE)
    operacion = models.ForeignKey(Operacion, on_delete=models.CASCADE, related_name='conjuntos')
    icono = models.ImageField(upload_to='iconos', blank=True, null=True)

    def __str__(self) -> str:
        return self.nombre

# Elementos de un conjunto de rodillos. Que rodillo en que posición dentro de un conjunto de rodillos
class Elemento(models.Model):
    nombre = models.CharField(max_length=50)
    conjunto = models.ForeignKey(Conjunto, on_delete=models.CASCADE, related_name='elementos')
    eje = models.ForeignKey(Eje, on_delete=models.CASCADE)
    rodillo = models.ForeignKey(Rodillo, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nombre

# Montaje
class Montaje(models.Model):
    nombre = models.CharField(max_length=50)
    maquina = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name='montajes')
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    bancadas = models.ManyToManyField(Bancada, related_name='montajes')

    def __str__(self) -> str:
        return self.nombre
    
# Planos de los rodillos
class Plano(models.Model):
    nombre = models.CharField(max_length=200)
    rodillos = models.ManyToManyField(Rodillo, related_name='planos')

    def __str__(self) -> str:
        return self.nombre

# Revisión: Modificaciones de un plano  
class Revision(models.Model):
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE)
    motivo = models.TextField(max_length=250)
    archivo = models.FileField(upload_to='planos')

#Instancia: Un rodillo en concreto
class Instancia(models.Model):
    nombre = models.CharField(max_length=200)
    rodillo = models.ForeignKey(Rodillo, on_delete=models.CASCADE)
    planos = models.ManyToManyField(Plano, related_name='instancias')