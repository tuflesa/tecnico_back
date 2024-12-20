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
    montajes = models.ManyToManyField(Montaje, related_name='articulos')

    def __str__(self) -> str:
        return self.nombre
    
# Variante. Todas las posiciones de los ejes de la máquina para un determinado Articulo y Montaje
class Variante(models.Model):
    nombre = models.CharField(max_length=50)
    montaje = models.ForeignKey(Montaje, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    # Pinch Roll
    pr_inf = models.FloatField(null=False, blank=False)
    pr_presion = models.FloatField(null=False, blank=False)
    # Break down - Formadora
    bd1_sup = models.FloatField(null=False, blank=False)
    bd1_inf = models.FloatField(null=False, blank=False)
    bd2_sup = models.FloatField(null=False, blank=False)
    bd2_inf = models.FloatField(null=False, blank=False)
    is1_ancho = models.FloatField(null=False, blank=False)
    is1_alto = models.FloatField(null=False, blank=False)
    # Lineal
    l_entrada_sup = models.FloatField(null=False, blank=False)
    l_entrada_ancho = models.FloatField(null=False, blank=False)
    l_entrada_alto = models.FloatField(null=False, blank=False)
    l_entrada_rod_inf = models.FloatField(null=False, blank=False)
    l_centro_rod_inf = models.FloatField(null=False, blank=False)
    l_saluda_sup = models.FloatField(null=False, blank=False)
    l_salida_ancho = models.FloatField(null=False, blank=False)
    l_salida_alto = models.FloatField(null=False, blank=False)
    l_salida_rod_inf = models.FloatField(null=False, blank=False)
    # Finpass - Cuchillas
    fp1_sup = models.FloatField(null=False, blank=False)
    fp1_inf = models.FloatField(null=False, blank=False)
    is2_ancho = models.FloatField(null=False, blank=False)
    is2_alto = models.FloatField(null=False, blank=False)
    fp2_sup = models.FloatField(null=False, blank=False)
    fp2_inf = models.FloatField(null=False, blank=False)
    is3_ancho = models.FloatField(null=False, blank=False)
    is3_alto = models.FloatField(null=False, blank=False)
    fp3_sup = models.FloatField(null=False, blank=False)
    fp3_inf = models.FloatField(null=False, blank=False)
    # Welding - Soldadura
    w_inf = models.FloatField(null=False, blank=False)
    w_lat_op = models.FloatField(null=False, blank=False)
    w_lat_mo = models.FloatField(null=False, blank=False)
    w_sup_op_v = models.FloatField(null=False, blank=False) # Eje vertical
    w_sup_op_h = models.FloatField(null=False, blank=False) # Eje horizontal
    w_sup_mo_v = models.FloatField(null=False, blank=False) # Eje vertical
    w_sup_mo_h = models.FloatField(null=False, blank=False) # Eje horizontal
    # Calibradora
    cb1_sup = models.FloatField(null=False, blank=False)
    cb1_inf = models.FloatField(null=False, blank=False)
    cb1_lat_op = models.FloatField(null=False, blank=False)
    cb1_lat_mo = models.FloatField(null=False, blank=False)
    cb2_sup = models.FloatField(null=False, blank=False)
    cb2_inf = models.FloatField(null=False, blank=False)
    cb2_lat_op = models.FloatField(null=False, blank=False)
    cb2_lat_mo = models.FloatField(null=False, blank=False)
    cb3_sup = models.FloatField(null=False, blank=False)
    cb3_inf = models.FloatField(null=False, blank=False)
    cb3_lat_op = models.FloatField(null=False, blank=False)
    cb3_lat_mo = models.FloatField(null=False, blank=False)
    cb4_sup = models.FloatField(null=False, blank=False)
    cb4_inf = models.FloatField(null=False, blank=False)
    cb4_lat_op = models.FloatField(null=False, blank=False)
    cb4_lat_mo = models.FloatField(null=False, blank=False)
