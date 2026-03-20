from django.db import models
from django.core.exceptions import ValidationError


# ─────────────────────────────────────────
# CONSTANTES DE GEOMETRÍA DEL FOSO
# ─────────────────────────────────────────
COLUMNAS_POR_ALTURA = {
    1: 9,
    2: 8,
    3: 9,
    4: 8,
    5: 9,
}


class Linea(models.Model):
    """Representa una línea dentro del foso."""
    nombre      = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    activa      = models.BooleanField(default=True)
    creada_en   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Línea"
        verbose_name_plural = "Líneas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Posicion(models.Model):
    """
    Celda física del foso.
    Cada combinación (linea, altura, columna) es única.
    La validación garantiza que columna no supere el máximo de esa altura.
    """
    linea   = models.ForeignKey(Linea, on_delete=models.CASCADE, related_name="posiciones")
    altura  = models.PositiveSmallIntegerField()   # 1–5
    columna = models.PositiveSmallIntegerField()   # 1–9 según altura

    class Meta:
        verbose_name = "Posición"
        verbose_name_plural = "Posiciones"
        unique_together = ("linea", "altura", "columna")
        ordering = ["linea", "altura", "columna"]

    def clean(self):
        if self.altura not in COLUMNAS_POR_ALTURA:
            raise ValidationError(f"Altura {self.altura} no válida. Debe ser entre 1 y 5.")
        max_col = COLUMNAS_POR_ALTURA[self.altura]
        if self.columna < 1 or self.columna > max_col:
            raise ValidationError(
                f"La columna {self.columna} no es válida para la altura {self.altura}. "
                f"Máximo permitido: {max_col}."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def max_columnas(self):
        return COLUMNAS_POR_ALTURA.get(self.altura, 0)

    @property
    def ocupacion_activa(self):
        return self.ocupaciones.filter(activo=True).first()

    def __str__(self):
        return f"{self.linea.nombre} — Altura {self.altura}, Col {self.columna}"


class Bobina(models.Model):
    """Datos propios de una bobina, independientes de su ubicación."""
    codigo          = models.CharField(max_length=100, unique=True)
    material        = models.CharField(max_length=200, blank=True, null=True)
    peso_kg         = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    diametro_mm     = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ancho_mm        = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    colada          = models.CharField(max_length=100, blank=True, null=True)
    proveedor       = models.CharField(max_length=200, blank=True, null=True)
    fecha_entrada   = models.DateField(blank=True, null=True)
    fecha_salida    = models.DateField(blank=True, null=True)
    observaciones   = models.TextField(blank=True, null=True)
    creada_en       = models.DateTimeField(auto_now_add=True)
    actualizada_en  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bobina"
        verbose_name_plural = "Bobinas"
        ordering = ["-creada_en"]

    @property
    def en_foso(self):
        """True si la bobina tiene una ocupación activa en este momento."""
        return self.ocupaciones.filter(activo=True).exists()

    @property
    def posicion_actual(self):
        """Devuelve la posición actual o None."""
        ocupacion = self.ocupaciones.filter(activo=True).first()
        return ocupacion.posicion if ocupacion else None

    def __str__(self):
        return f"Bobina {self.codigo}"


class Ocupacion(models.Model):
    """
    Relaciona una Bobina con una Posicion en un período de tiempo.
    Solo puede haber UNA ocupación activa por posición.
    Historial completo: posicion → bobinas que pasaron por ella.
                        bobina   → posiciones donde ha estado.
    """
    posicion     = models.ForeignKey(Posicion, on_delete=models.PROTECT, related_name="ocupaciones")
    bobina       = models.ForeignKey(Bobina,   on_delete=models.PROTECT, related_name="ocupaciones")
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin    = models.DateTimeField(blank=True, null=True)
    activo       = models.BooleanField(default=True)
    notas        = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Ocupación"
        verbose_name_plural = "Ocupaciones"
        ordering = ["-fecha_inicio"]

    def clean(self):
        # Solo una ocupación activa por posición
        if self.activo:
            qs = Ocupacion.objects.filter(posicion=self.posicion, activo=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    f"La posición {self.posicion} ya tiene una bobina activa."
                )
        # Solo una ocupación activa por bobina
        if self.activo:
            qs = Ocupacion.objects.filter(bobina=self.bobina, activo=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    f"La bobina {self.bobina} ya está colocada en otra posición."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        estado = "activa" if self.activo else "finalizada"
        return f"{self.bobina} en {self.posicion} [{estado}]"