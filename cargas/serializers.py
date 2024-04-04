from rest_framework import serializers
from .models import Agencia, Bascula, Carga, Llamada
from estructura.serializers import EmpresaSerializer

class AgenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agencia
        fields = ['id', 'nombre', 'telefono', 'contacto', 'observaciones']

class BasculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bascula
        fields = ['id', 'nombre', 'empresa', 'url']

class CargaSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(many=False)
    agencia = AgenciaSerializer(many=False)
    fecha_entrada = serializers.DateField(format="%d-%m-%Y")
    hora_entrada =serializers.TimeField(format="%H:%M")
    fecha_salida = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    class Meta:
        model = Carga
        fields = ['id', 'empresa', 'matricula', 'remolque', 'agencia', 'telefono', 'fecha_entrada', 'hora_entrada', 'tara', 'destino', 'bruto', 'fecha_salida', 'puerta', 'observaciones']

class CargaSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carga
        fields = ['id', 'empresa', 'matricula', 'remolque', 'agencia', 'telefono', 'fecha_entrada', 'hora_entrada', 'tara', 'destino', 'bruto', 'fecha_salida', 'puerta', 'observaciones']

class LlamadaSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Llamada
        fields = ['id', 'carga', 'fecha', 'hora', 'puerta']

class UltimasLlamadasSerializer(serializers.ModelSerializer):
    carga = CargaSerializer(many=False)
    fecha = serializers.DateField(format="%d-%m-%Y")
    hora = serializers.TimeField(format="%H:%M")
    class Meta:
        model = Llamada
        fields = ['id', 'carga', 'fecha', 'hora', 'puerta']
