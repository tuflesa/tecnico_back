from django.db import models

class Empresa(models.Model):
    nombre = models.CharField(max_length=20)
    siglas = models.CharField(max_length=10, blank=True, null=True)    
    logo = models.ImageField(upload_to='logos', null=True)
    direccion = models.CharField(max_length=80, blank=True, null=True)
    poblacion = models.CharField(max_length=50, blank=True, null=True)
    codpostal = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    cif = models.CharField(max_length=9, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Direcciones(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name= 'direcciones')
    direccion = models.CharField(max_length=80, blank=True, null=True)
    poblacion = models.CharField(max_length=50, blank=True, null=True)
    codpostal = models.CharField(max_length=8, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    provincia = models.CharField(max_length=50, blank=True, null=True)
    cif = models.CharField(max_length=9, blank=True, null=True)

class Zona(models.Model): # máquinas
    nombre = models.CharField(max_length=50)
    siglas = models.CharField(max_length=10, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='zonas')
    es_maquina_tubo = models.BooleanField(default=True)
    espesor_1 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    espesor_2 = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.empresa.siglas + '-' + self.nombre
    def empresa_id(self):
        return self.empresa.id

class Seccion(models.Model):
    nombre = models.CharField(max_length=50)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name='secciones')

    def siglas_zona(self):
        return self.zona.siglas

    def empresa_id(self):
        return self.zona.empresa.id

    def __str__(self):
        return self.zona.siglas + '-' + self.nombre

class Equipo(models.Model):
    nombre = models.CharField(max_length=50)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='equipos')
    fabricante = models.CharField(max_length=50, null=True, blank=True)
    modelo = models.CharField(max_length=50, null=True, blank=True)
    numero = models.CharField(max_length=50, null=True, blank=True)
    imagen = models.ImageField(upload_to='equipos', blank=True, null=True)

    def siglas_zona(self):
        return self.seccion.zona.siglas

    def zona_id(self):
        return self.seccion.zona.id

    def empresa_id(self):
        return self.seccion.zona.empresa.id

    def seccion_nombre(self):
        return self.seccion.nombre

    def __str__(self):
        return str(self.seccion) + '-' + self.nombre