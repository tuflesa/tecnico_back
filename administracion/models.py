from django.db import models
from django.contrib.auth.models import User
from estructura.models import Empresa, Zona, Seccion

class Aplicacion(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=200)
    imagen = models.ImageField(upload_to='administracion')
    url = models.CharField(max_length=50)
    usuarios = models.ManyToManyField(User)

    def __str__(self):
        return self.nombre

class Puesto(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
class NivelAcceso(models.Model):
    nombre = models.CharField(max_length=20) 
    descripcion = models.TextField(max_length=200)

    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    zona = models.ForeignKey(Zona, null=True, blank=True, on_delete=models.CASCADE)
    seccion = models.ForeignKey(Seccion, null=True, blank=True, on_delete=models.CASCADE)
    puesto = models.ForeignKey(Puesto, on_delete=models.CASCADE)
    nivel_acceso = models.ForeignKey(NivelAcceso, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.get_full_name() 