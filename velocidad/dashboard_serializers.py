from rest_framework import serializers
from .models import Parada, Periodo, Turnos

class TurnoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turnos
        fields = ['id', 'turno']

class PeriodoOEESerializer(serializers.ModelSerializer):
    turno = TurnoSimpleSerializer()

    class Meta:
        model = Periodo
        fields = ['inicio', 'fin', 'velocidad', 'vmax', 'turno']

class ParadaOEESerializer(serializers.ModelSerializer):
    periodos        = PeriodoOEESerializer(many=True)
    tipo_parada     = serializers.CharField(source='codigo.tipo.nombre')
    tipo_parada_id  = serializers.IntegerField(source='codigo.tipo.id')

    class Meta:
        model = Parada
        fields = ['id', 'tipo_parada', 'tipo_parada_id', 'periodos']