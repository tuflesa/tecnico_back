from django.db import models
from rodillos.models import Montaje

# Formas del tubo
class Formas(models.Model): # Redondo, Cuadrado, Rectangular
    nombre = models.CharField(max_length=20)
    siglas = models.CharField(max_length=5, null=False, blank=False)

    def __str__(self) -> str:
        return self.nombre    
    
# Calidad
class Calidad(models.Model): # S235, S355, etc
    nombre = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.nombre 
    
# Acabado superficial
class Acabado(models.Model): # Negro, Decapado, Galvanizado
    nombre = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.nombre
    
# Norma
class Norma(models.Model): # EN10.219, EN10305, 
    nombre = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.nombre

# Articulo
class Articulo(models.Model): # Ejemplo Red. 100x3.0 S275 Negro EN10.219
    nombre = models.CharField(max_length=50)
    forma = models.ForeignKey(Formas, on_delete=models.CASCADE)
    dim1 = models.CharField(max_length=5) # 0 si es redondo
    dim2 = models.CharField(max_length=5)
    espesor = models.CharField(max_length=4)
    calidad = models.ForeignKey(Calidad, on_delete=models.CASCADE)
    acabado = models.ForeignKey(Acabado, on_delete=models.CASCADE)
    norma = models.ForeignKey(Norma, on_delete=models.CASCADE)
    desarrollo = models.IntegerField()
    montajes = models.ManyToManyField(Montaje, related_name='articulos')

    def __str__(self) -> str:
        return self.nombre
