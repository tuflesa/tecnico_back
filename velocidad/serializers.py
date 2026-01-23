from rest_framework import serializers
from .models import ZonaPerfilVelocidad, Registro, Periodo, Parada, HorarioDia, TipoParada, CodigoParada, DestrezasVelocidad
from estructura.serializers import ZonaSerializer

class ZonaPerfilVelocidadSerilizer(serializers.ModelSerializer):
    zona = ZonaSerializer(many=False)
    class Meta:
        model = ZonaPerfilVelocidad
        fields = ['id', 'zona', 'ip', 'rack', 'slot', 'db', 'dw', 'nwords', 'color', 'v_max', 'hf_pmax', 'hf_fmax', 'hf_fmin', 'fuerza_max', 'control_paradas']

class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro
        fields = ['id', 'fecha', 'hora', 'zona', 'velocidad', 'potencia', 'frecuencia', 'presion']

class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = '__all__'

class ParadasActualizarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parada
        fields = '__all__'

class ParadaSerializer(serializers.ModelSerializer):
    inicio = serializers.SerializerMethodField()
    fin = serializers.SerializerMethodField()
    duracion = serializers.SerializerMethodField()
    codigo = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    class Meta:
        model = Parada
        fields = ['id', 'codigo', 'zona', 'observaciones', 'inicio', 'fin', 'duracion', 'color']
    
    def get_codigo(self, obj):
        return obj.codigo.nombre
    
    def get_color(self, obj):
        return obj.codigo.tipo.color
        
    def get_inicio(self, obj):
        return obj.inicio()

    def get_fin(self, obj):
        return obj.fin()

    def get_duracion(self, obj):
        return obj.duracion()


class HorarioDiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioDia
        fields = '__all__'

class TipoParadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoParada
        fields = '__all__'

class CodigoParadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodigoParada
        fields = '__all__'

class DestrezasVelocidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestrezasVelocidad
        fields = ['id', 'nombre']