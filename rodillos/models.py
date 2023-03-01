from django.db import models
from estructura.models import Empresa

# Máquinas de tubo
class Maquina(models.Model):
    nombre = models.CharField(max_length=50)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='maquinas')

    def __str__(self):
        return self.nombre

# Secciones de una máquina: Formadora, cuchillas, calibradora, etc
class Seccion(models.Model):
    nombre = models.CharField(max_length=50)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='secciones')

    def __str__(self):
        return self.nombre

# Operaciones de una sección
class Operacion(models.Model):
    nombre = models.CharField(max_length=50) # Ejemplo: 1ªOP Formadora
    siglas = models.CharField(max_length=4) # Ejemplo: F1
    seccion = models.Model(Seccion, on_delete=models.CASCADE, related_name='operaciones') 
    icono = models.ImageField(upload_to='operaciones', blank=True, null=True) 

    def __str__(self):
        return self.nombre

# Posición dentro de una operación
class Posicion(models.Model):
    nombre = models.CharField(max_length=50) # Ejemplos: superior, inferior, lateral, ...
    operacion = models.ForeignKey(Operacion, on_delete=models.CASCADE, related_name='posiciones')

    def __str__(self):
        return self.operacion.nombre + ' - ' + self.nombre

# Materiales de los que están hechos los rodillos: Ejemplos 1.2379, AMPCO, Ceramica, etc
class Material(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.nombre

# Rodillos de una posición
class Rodillo(models.Model):
    nombre = models.CharField(max_length=50)
    posicion = models.ForeignKey(Posicion, on_delete=models.CASCADE, related_name='rodillos')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nombre

# Ficheros asociados a un rodillo: Planos, CNC, etc
class Ficheros(models.Model):
    nombre = models.CharField(max_length=50)
    rodillo = models.ForeignKey(Rodillo, on_delete=models.CASCADE, related_name='ficheros')
    fichero = models.FileField(upload_to='ficheros')

    def __str__(self) -> str:
        return self.nombre