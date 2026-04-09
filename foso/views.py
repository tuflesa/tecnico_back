from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Foso, Linea, Posicion, Bobina, Ocupacion, Material, Proveedor
from .serializers import (
    FosoSerializer, FosoLineaSerializer,
    LineaSerializer, PosicionSerializer,
    BobinaSerializer, OcupacionSerializer,
    ColocarBobinaSerializer, MaterialSerializer, ProveedorSerializer
)


class FosoViewSet(viewsets.ModelViewSet):
    queryset = Foso.objects.select_related("empresa").all()
    serializer_class = FosoSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        empresa_id = self.request.query_params.get("empresa")
        if empresa_id:
            qs = qs.filter(empresa_id=empresa_id)
        return qs

    @action(detail=True, methods=["get"], url_path="grid")
    def grid(self, request, pk=None):
        """
        GET /api/fosos/{id}/grid/
        Devuelve todas las líneas del foso con su grid completo.
        """
        foso = self.get_object()
        lineas = foso.lineas.filter(activa=True)
        serializer = FosoLineaSerializer(lineas, many=True)
        return Response(serializer.data)


class LineaViewSet(viewsets.ModelViewSet):
    queryset = Linea.objects.select_related("foso__empresa").all()
    serializer_class = LineaSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        foso_id = self.request.query_params.get("foso")
        if foso_id:
            qs = qs.filter(foso_id=foso_id)
        return qs

    @action(detail=True, methods=["get"], url_path="grid")
    def grid(self, request, pk=None):
        """
        GET /api/lineas/{id}/grid/
        Grid completo de una línea concreta.
        """
        linea = self.get_object()
        serializer = FosoLineaSerializer(linea)
        return Response(serializer.data)


class PosicionViewSet(viewsets.ModelViewSet):
    queryset = Posicion.objects.select_related("linea__foso").all()
    serializer_class = PosicionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        linea_id = self.request.query_params.get("linea")
        foso_id  = self.request.query_params.get("foso")
        if linea_id:
            qs = qs.filter(linea_id=linea_id)
        if foso_id:
            qs = qs.filter(linea__foso_id=foso_id)
        return qs


class BobinaViewSet(viewsets.ModelViewSet):
    queryset = Bobina.objects.select_related("material", "proveedor").all()
    serializer_class = BobinaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['codigo', 'colada', 'material__nombre', 'proveedor__nombre']

    @action(detail=True, methods=["get"], url_path="historial")
    def historial(self, request, pk=None):
        """
        GET /api/bobinas/{id}/historial/
        Todas las posiciones por donde pasó la bobina.
        """
        bobina = self.get_object()
        ocupaciones = bobina.ocupaciones.select_related(
            "posicion__linea__foso"
        ).order_by("-fecha_inicio")
        serializer = OcupacionSerializer(ocupaciones, many=True)
        return Response(serializer.data)


class OcupacionViewSet(viewsets.ModelViewSet):
    queryset = Ocupacion.objects.select_related(
        "posicion__linea__foso", "bobina"
    ).all()
    serializer_class = OcupacionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        foso_id = self.request.query_params.get("foso")
        if foso_id:
            qs = qs.filter(posicion__linea__foso_id=foso_id)
        return qs

    @action(detail=False, methods=["post"], url_path="colocar")
    def colocar(self, request):
        """
        POST /api/ocupaciones/colocar/
        Coloca una bobina en una posición.
        Si la bobina ya estaba en otro sitio, cierra esa ocupación primero.
        """
        ser = ColocarBobinaSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        bobina   = Bobina.objects.get(pk=ser.validated_data["bobina_id"])
        posicion = Posicion.objects.get(pk=ser.validated_data["posicion_id"])
        notas    = ser.validated_data.get("notas", "")

        # Cerrar ocupación activa de la posición destino (si existe)
        Ocupacion.objects.filter(posicion=posicion, activo=True).update(
            activo=False, fecha_fin=timezone.now()
        )
        # Cerrar ocupación activa de la bobina (si está en otro sitio)
        Ocupacion.objects.filter(bobina=bobina, activo=True).update(
            activo=False, fecha_fin=timezone.now()
        )

        nueva = Ocupacion.objects.create(
            posicion=posicion,
            bobina=bobina,
            activo=True,
            notas=notas,
        )
        return Response(OcupacionSerializer(nueva).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="retirar")
    def retirar(self, request, pk=None):
        """POST /api/ocupaciones/{id}/retirar/  →  cierra la ocupación."""
        ocupacion = self.get_object()
        if not ocupacion.activo:
            return Response({"detail": "La ocupación ya estaba cerrada."}, status=400)
        ocupacion.activo    = False
        ocupacion.fecha_fin = timezone.now()
        ocupacion.save()
        return Response(OcupacionSerializer(ocupacion).data)


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer