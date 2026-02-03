from rest_framework import serializers
from .models import ZonaPerfilVelocidad, Registro, Periodo, Parada, HorarioDia, TipoParada, CodigoParada, DestrezasVelocidad, PalabrasClave
from estructura.serializers import ZonaSerializer
from django.utils import timezone

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

class PeriodoCrearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = ['id', 'inicio', 'fin', 'velocidad', 'parada']
        read_only_fields = ['parada']

    def validate_inicio(self, value):
            # Si ya viene con zona horaria (aware), no hacemos nada.
            # Solo aplicamos la del sistema si viene vacía (naive).
            if timezone.is_naive(value):
                return timezone.make_aware(value, timezone.get_current_timezone())
            return value

    def validate_fin(self, value):
        if timezone.is_naive(value):
            return timezone.make_aware(value, timezone.get_current_timezone())
        return value

class ParadasCrearSerializer(serializers.ModelSerializer):
    periodos = PeriodoCrearSerializer(many=True, required=False)

    class Meta:
        model = Parada
        fields = ['id', 'codigo', 'zona', 'observaciones', 'periodos']

    def create(self, validated_data):
        periodos_data = validated_data.pop('periodos', [])
        parada = Parada.objects.create(**validated_data)
        for periodo in periodos_data:
            # Aquí asignamos la parada manualmente
            Periodo.objects.create(parada=parada, **periodo)
        return parada

    def update(self, instance, validated_data):
        periodos_data = validated_data.pop('periodos', None)
        
        # Actualizar campos básicos de la parada
        instance.codigo = validated_data.get('codigo', instance.codigo)
        instance.zona = validated_data.get('zona', instance.zona)
        instance.observaciones = validated_data.get('observaciones', instance.observaciones)
        instance.save()

        if periodos_data is not None:
            # Borramos periodos antiguos y creamos los nuevos según la lógica de división
            instance.periodos.all().delete()
            for p_data in periodos_data:
                Periodo.objects.create(parada=instance, **p_data)
        
        return instance

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

class PalabrasClaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalabrasClave
        fields = '__all__'