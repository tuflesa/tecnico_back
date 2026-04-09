from django.db import models
from django.core.exceptions import ValidationError


class Foso(models.Model):
    """
    Foso físico perteneciente a una empresa.
    columnas_por_altura define la geometría propia de este foso.
    Ejemplo: {1: 9, 2: 8, 3: 9, 4: 8, 5: 9}
    """
    empresa = models.ForeignKey(
        'estructura.Empresa',
        on_delete=models.CASCADE,
        related_name='fosos'
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    columnas_por_altura = models.JSONField(
        default=dict,
        help_text='Ej: {"1": 9, "2": 8, "3": 9, "4": 8, "5": 9}'
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Foso"
        verbose_name_plural = "Fosos"
        ordering = ["empresa", "nombre"]

    def get_max_columnas(self, altura):
        """Devuelve el máximo de columnas para una altura dada."""
        return self.columnas_por_altura.get(str(altura), 0)

    def __str__(self):
        return f"{self.empresa} — {self.nombre}"


class Linea(models.Model):
    """Representa una línea dentro de un foso."""
    foso = models.ForeignKey(Foso, on_delete=models.CASCADE, related_name='lineas')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Línea"
        verbose_name_plural = "Líneas"
        ordering = ["foso", "nombre"]

    def __str__(self):
        return f"{self.foso} — {self.nombre}"


class Posicion(models.Model):
    """
    Celda física del foso.
    La validación lee la geometría del foso al que pertenece la línea.
    """
    linea = models.ForeignKey(Linea, on_delete=models.CASCADE, related_name="posiciones")
    altura = models.PositiveSmallIntegerField()
    columna = models.PositiveSmallIntegerField()
    habilitada = models.BooleanField(default=True)
    motivo_anulacion = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Motivo por el que la posición no se puede usar"
    )

    class Meta:
        verbose_name = "Posición"
        verbose_name_plural = "Posiciones"
        unique_together = ("linea", "altura", "columna")
        ordering = ["linea", "altura", "columna"]

    def clean(self):
        foso = self.linea.foso
        max_col = foso.get_max_columnas(self.altura)

        if max_col == 0:
            raise ValidationError(
                f"La altura {self.altura} no está definida en la geometría del foso '{foso}'."
            )
        if self.columna < 1 or self.columna > max_col:
            raise ValidationError(
                f"La columna {self.columna} no es válida para la altura {self.altura} "
                f"en el foso '{foso}'. Máximo permitido: {max_col}."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def max_columnas(self):
        return self.linea.foso.get_max_columnas(self.altura)

    @property
    def ocupacion_activa(self):
        return self.ocupaciones.filter(activo=True).first()

    def __str__(self):
        return f"{self.linea} — Altura {self.altura}, Col {self.columna}"


class Material(models.Model):
    nombre = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Bobina(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    material = models.ForeignKey('Material', on_delete=models.SET_NULL, blank=True, null=True)
    peso_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ref_proveedor = models.CharField(max_length=200, blank=True, null=True)
    ancho_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    colada = models.CharField(max_length=100, blank=True, null=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, blank=True, null=True)
    fecha_entrada = models.DateField(auto_now_add=True)
    fecha_salida = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)
    espesor_mm = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "Bobina"
        verbose_name_plural = "Bobinas"
        ordering = ["-creada_en"]

    @property
    def en_foso(self):
        return self.ocupaciones.filter(activo=True).exists()

    @property
    def posicion_actual(self):
        ocupacion = self.ocupaciones.filter(activo=True).first()
        return ocupacion.posicion if ocupacion else None

    def __str__(self):
        return f"Bobina {self.codigo}"


class Ocupacion(models.Model):
    posicion = models.ForeignKey(Posicion, on_delete=models.PROTECT, related_name="ocupaciones")
    bobina = models.ForeignKey(Bobina, on_delete=models.PROTECT, related_name="ocupaciones")
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    notas = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Ocupación"
        verbose_name_plural = "Ocupaciones"
        ordering = ["-fecha_inicio"]

    def clean(self):
        if not self.posicion.habilitada:
            raise ValidationError(
                f"La posición {self.posicion} está anulada y no se puede ocupar.")
        if self.activo:
            qs = Ocupacion.objects.filter(posicion=self.posicion, activo=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    f"La posición {self.posicion} ya tiene una bobina activa.")
        if self.activo:
            qs = Ocupacion.objects.filter(bobina=self.bobina, activo=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    f"La bobina {self.bobina} ya está colocada en otra posición.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        estado = "activa" if self.activo else "finalizada"
        return f"{self.bobina} en {self.posicion} [{estado}]"


class DestrezasFoso(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Destreza"
        verbose_name_plural = "Destrezas"

    def __str__(self):
        return self.nombre