from django.db import models

class Empresa(models.Model):
    nombre = models.CharField(max_length=20)
    siglas = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.nombre

class Zona(models.Model):
    nombre = models.CharField(max_length=50)
    siglas = models.CharField(max_length=10, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='zonas')

    def __str__(self):
        return self.empresa.siglas + '-' + self.nombre

class Seccion(models.Model):
    nombre = models.CharField(max_length=50)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name='secciones')

    def __str__(self):
        return self.zona.siglas + '-' + self.nombre

class Equipo(models.Model):
    nombre = models.CharField(max_length=50)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='equipos')
    fabricante = models.CharField(max_length=50, null=True, blank=True)
    modelo = models.CharField(max_length=50, null=True, blank=True)
    numero = models.CharField(max_length=50, null=True, blank=True)
    imagen = models.ImageField(upload_to='equipos', blank=True)

    def __str__(self):
        return str(self.seccion) + '-' + self.nombre