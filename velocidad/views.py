from rest_framework import viewsets
from django.http import JsonResponse
from django_filters import rest_framework as filters
from .serializers import RegistroSerializer, ZonaPerfilVelocidadSerilizer, HorarioDiaSerializer, TipoParadaSerializer, CodigoParadaSerializer, ParadaSerializer, DestrezasVelocidadSerializer, ParadasActualizarSerializer, ParadasCrearSerializer, PeriodoSerializer, PalabrasClaveSerializer, TurnosSerializer
from .models import Registro, ZonaPerfilVelocidad, Parada, CodigoParada, Periodo, HorarioDia, TipoParada, Periodo, DestrezasVelocidad, PalabrasClave, Turnos
from estructura.models import Zona
from trazabilidad.models import Flejes, Tubos, OF
from django.forms.models import model_to_dict
from django.db.models import Q
from django.db.models import Min, Max
from datetime import datetime, date, time
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .calendario import generar_horario_anual
from types import SimpleNamespace

class DestrezasVelocidadFilter(filters.FilterSet):
    class Meta:
        model = DestrezasVelocidad
        fields = {
            'nombre': ['icontains'],
            'nombre': ['exact'],
            'id': ['exact'],
        }
class RegistroFilter(filters.FilterSet):
    class Meta:
        model = Registro
        fields = {
            'zona__empresa': ['exact'],
            'fecha': ['exact'],
            'hora': ['gte', 'lte']
        }

class PeriodoFilter(filters.FilterSet):
    class Meta:
        model = Periodo
        fields = {
            'parada': ['exact'],
        }

class PalabrasClaveFilter(filters.FilterSet):
    class Meta:
        model = PalabrasClave
        fields = {
            'nombre': ['exact'],
            'zona': ['exact'],
        }

class ZonaPerfilVelocidadFilter(filters.FilterSet):
    class Meta:
        model = ZonaPerfilVelocidad
        fields = {
            'zona__empresa': ['exact'],
            'id': ['exact'],
        }

class HorarioDiaFilter(filters.FilterSet):
    class Meta:
        model = HorarioDia
        fields = {
            'fecha': ['exact'],
            'zona': ['exact']
        }

class TipoParadaFilter(filters.FilterSet):
    class Meta:
        model = TipoParada
        fields = {
            'para_informar': ['exact'],
        }

class CodigoParadaFilter(filters.FilterSet):
    class Meta:
        model = CodigoParada
        fields = {
            'nombre': ['icontains'],
        }

class TurnosFilter(filters.FilterSet):
    class Meta:
        model = Turnos
        fields = {
            'zona': ['exact'],
        }

class ParadaActualizarViewSet(viewsets.ModelViewSet):
    serializer_class = ParadasActualizarSerializer
    queryset = Parada.objects.all()

class ParadaCrearViewSet(viewsets.ModelViewSet):
    #serializer_class = ParadasCrearSerializer
    queryset = Parada.objects.all()
    def get_serializer_class(self):
        if self.action == 'create':
            return ParadasCrearSerializer
        elif self.action in ['update', 'partial_update']:
            return ParadasActualizarSerializer
        return ParadasCrearSerializer

class TipoParadaViewSet(viewsets.ModelViewSet):
    serializer_class = TipoParadaSerializer
    queryset = TipoParada.objects.all()
    filterset_class = TipoParadaFilter

class CodigoParadaViewSet(viewsets.ModelViewSet):
    serializer_class = CodigoParadaSerializer
    queryset = CodigoParada.objects.all()
    filterset_class = CodigoParadaFilter

class ZonaPerfilVelocidadViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ZonaPerfilVelocidadSerilizer
    queryset = ZonaPerfilVelocidad.objects.all()
    filterset_class = ZonaPerfilVelocidadFilter

class RegistroViewSet(viewsets.ModelViewSet):
    serializer_class = RegistroSerializer
    queryset = Registro.objects.all().order_by('fecha', 'hora')
    filterset_class = RegistroFilter

class HorarioDiaViewSet(viewsets.ModelViewSet):
    serializer_class = HorarioDiaSerializer
    queryset = HorarioDia.objects.all()
    filterset_class = HorarioDiaFilter

class DestrezasVelocidadViewSet(viewsets.ModelViewSet):
    serializer_class = DestrezasVelocidadSerializer
    queryset = DestrezasVelocidad.objects.all()
    filterset_class = DestrezasVelocidadFilter

class PeriodoViewSet(viewsets.ModelViewSet):
    serializer_class = PeriodoSerializer
    queryset = Periodo.objects.all()
    filterset_class = PeriodoFilter

class TurnosViewSet(viewsets.ModelViewSet):
    serializer_class = TurnosSerializer
    queryset = Turnos.objects.all()
    filterset_class = TurnosFilter

def estado_maquina(request, id):
    fecha_str = request.GET.get('fecha')
    fecha_fin_str = request.GET.get('fecha_fin')
    hora_inicio_str = request.GET.get('hora_inicio')
    hora_fin_str = request.GET.get('hora_fin')

    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
        hora_fin = datetime.strptime(hora_fin_str, '%H:%M').time()
        fecha_inico_dt = datetime.combine(fecha, hora_inicio)
        fecha_fin_dt = datetime.combine(fecha_fin, hora_fin)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Formato de hora inválido'}, status=400)


    # Datos de la máquina
    zona = Zona.objects.get(id=id)
    maquina = ZonaPerfilVelocidad.objects.get(zona=zona)
    maquina_dict = model_to_dict(maquina)
    zona_dict = model_to_dict(zona)
    maquina_dict['zona'] = zona_dict


    # Registros de velocidad
    from itertools import chain

    if (fecha != fecha_fin):
        registros = Registro.objects.filter(
        zona=id
        ).filter(
            Q(fecha__gt=fecha, fecha__lt=fecha_fin) |
            Q(fecha=fecha, hora__gte=hora_inicio) |
            Q(fecha=fecha_fin, hora__lte=hora_fin)
        ).order_by('fecha', 'hora')
    else:
        registros = Registro.objects.filter(
        zona=id
        ).filter(
            Q(fecha=fecha, hora__gte=hora_inicio, hora__lte=hora_fin)
        ).order_by('fecha', 'hora')

    # Obtener el registro anterior si hay resultados
    anterior = Registro.objects.filter(
        zona=id
    ).filter(
        Q(fecha__lt=fecha) |
        Q(fecha=fecha, hora__lt=hora_inicio)
    ).order_by('-fecha', '-hora').first()


    if anterior:
        registros = list(chain([anterior], registros))

    regs = [{
        'fecha': r.fecha.isoformat(),
        'hora': r.hora.isoformat(),
        'zona': r.zona.siglas,
        'velocidad':  float(r.velocidad),
        'potencia': float(r.potencia),
        'frecuencia': float(r.frecuencia),
        'presion': float(r.presion)
    } for r in registros]

    # Ordenes de fabricación
    resultado = OF.objects.filter(
        zona=id
    ).filter(
        Q(inicio__gte=fecha_inico_dt, fin__lte=fecha_fin_dt) |
        Q(fin__gte=fecha_inico_dt, fin__lte=fecha_fin_dt) |
        Q(inicio__gte=fecha_inico_dt, inicio__lte=fecha_fin_dt) |
        Q(inicio__lte=fecha_fin_dt, fin__isnull=True) 
    ).distinct().order_by('-inicio')
    # Serializar resultados
    OFs = [{
        'numero': of.numero,
        'inicio': of.inicio.isoformat() if of.inicio else None,
        'fin': of.fin.isoformat() if of.fin else None
    } for of in resultado]

    # Flejes fabricados
    siglas = maquina.zona.siglas.upper()
    resultado = Flejes.objects.filter(
        maquina_siglas=siglas
    ).filter(
        Q(fecha_entrada__gte=fecha, fecha_entrada__lte=fecha_fin) |
        Q(fecha_salida__gte=fecha, fecha_salida__lte=fecha_fin) |
        Q(fecha_entrada__gte=fecha, fecha_entrada__lte=fecha_fin) |
        Q(fecha_entrada__lte=fecha_fin, fecha_salida__isnull=True)  # En proceso
    ).distinct().order_by('-fecha_entrada', '-hora_entrada')
    # Serializar resultados
    flejes = [{
        'id': f.id,
        'pos': f.pos,
        'idProduccion': f.idProduccion,
        'IdArticulo': f.IdArticulo,
        'peso': f.peso,
        'of': f.of,
        'maquina_siglas': f.maquina_siglas,
        'descripcion': f.descripcion,
        'fecha_entrada': f.fecha_entrada.isoformat() if f.fecha_entrada else None,
        'hora_entrada': f.hora_entrada.isoformat() if f.hora_entrada else None,
        'fecha_salida': f.fecha_salida.isoformat() if f.fecha_salida else None,
        'hora_salida': f.hora_salida.isoformat() if f.hora_salida else None,
        'finalizada': f.finalizada,
        'ancho': f.ancho(),
        'espesor': f.espesor(),
        'metros_teorico': f.metros_teorico(),
        'metros_medido': f.metros_medido,
        'metros_tubo': f.metros_tubo(),
        'tubos': [{
            'n_tubos': t.n_tubos,
            'largo': t.largo,
            'descripcion': t.descripcion()
        } for t in f.tubos.all()]
    } for f in resultado]

    # Tubos fabricados
    resultado = Tubos.objects.filter(
        fleje__maquina_siglas=siglas
    ).filter(
        Q(fleje__fecha_entrada__gte=fecha, fleje__fecha_entrada__lte=fecha_fin) |
        Q(fleje__fecha_salida__gte=fecha, fleje__fecha_salida__lte=fecha_fin) |
        Q(fleje__fecha_entrada__lte=fecha_fin, fleje__fecha_salida__isnull=True) 
    ).distinct().order_by('-fleje__fecha_entrada', '-fleje__hora_entrada')
    # Serializar resultados
    tubos = [{
        'descripcion': t.descripcion(),
        'n_tubos': t.n_tubos
    } for t in resultado]
    

    # Estado actual
    # Fleje y Tubo actual
    estado_act = Registro.objects.filter(zona=id).last()
    fleje_act = Flejes.objects.filter(maquina_siglas=siglas, fecha_salida__isnull=True).order_by('-fecha_entrada', '-hora_entrada').last()
    if (fleje_act == None):
        fleje_act = SimpleNamespace(
            of='',
            pos='',
            descripcion=''
        )
        tubo_act = SimpleNamespace(
            n_tubos='',
            descripcion=''
        )
    else:
        tubo_actual = Tubos.objects.filter(fleje=fleje_act).last()
        if(tubo_actual == None):
            tubo_act = SimpleNamespace(
                n_tubos='',
                descripcion=''
            )
        else:
            tubo_act = SimpleNamespace(
                n_tubos = tubo_actual.n_tubos,
                descripcion = tubo_actual.descripcion()
            )
    # OF Actual
    OF_actual = OF.objects.filter(zona=id).last()
    if (OF_actual == None):
        current_of =  fleje_act.of
    else:
        current_of = OF_actual.numero

    estado_act = {
        'velocidad':  float(estado_act.velocidad),
        'potencia': float(estado_act.potencia),
        'frecuencia': float(estado_act.frecuencia),
        'fuerza': float(estado_act.presion),
        'of': current_of,
        'fleje_pos': fleje_act.pos,
        'fleje_descripcion': fleje_act.descripcion,
        'n_tubos': tubo_act.n_tubos,
        'tubo_descripcion': tubo_act.descripcion
    }

    # Paradas
    inicio_str = fecha_str + ' ' + hora_inicio_str
    inicio_dt = datetime.strptime(inicio_str, "%Y-%m-%d %H:%M")
    inicio_dt = timezone.make_aware(inicio_dt, timezone.utc)

    fin_str = fecha_fin_str + ' ' + hora_fin_str
    fin_dt = datetime.strptime(fin_str, "%Y-%m-%d %H:%M")
    fin_dt = timezone.make_aware(fin_dt, timezone.utc)
    resultado = Parada.objects.filter(
        Q(zona=id, periodos__inicio__gte=inicio_dt, periodos__inicio__lte=fin_dt) |
        Q(zona=id, periodos__fin__gte=inicio_dt, periodos__fin__lte=fin_dt) 
    ).annotate(
    # Para que no repita por cada periodo la parada ya que pueden estar unidas y ser la misma
    fecha_referencia=Min('periodos__inicio')
    ).distinct().order_by('-fecha_referencia')

    paradas = [{
        'id': p.id,
        'codigo': p.codigo.nombre,
        'codigo_id': p.codigo.id,
        'tipo_parada_id':p.codigo.tipo.id,
        'inicio': p.inicio().strftime("%Y-%m-%d %H:%M:%S") if p.inicio else None,
        'fin': p.fin().strftime("%Y-%m-%d %H:%M:%S") if p.fin else None,
        'duracion': p.duracion(),
        'color': p.codigo.tipo.color,
        'observaciones': p.observaciones,
        'zona_id': p.zona.id,
        'palabraclave_id':p.codigo.palabra_clave.id if p.codigo.palabra_clave else "",
        'palabra_clave': p.codigo.palabra_clave.nombre if p.codigo.palabra_clave else "",
        'tipo_parada_nombre':p.codigo.tipo.nombre,
    } for p in resultado]
    
    data = {
        "maquina": maquina_dict,
        "registros": regs,
        "flejes": flejes,
        "estado_act": estado_act,
        "paradas": paradas,
        "tubos": tubos,
        "OFs": OFs
    }
    return JsonResponse(data)

@api_view(['POST'])
def nuevo_periodo(request):
    datos = request.data
    fecha_str = datos['fecha']
    fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
    fecha_dt = timezone.make_aware(fecha_dt, timezone.utc)
    zona_id = datos['zona']
    velocidad = float(datos['velocidad'])
    tnp = datos['tnp'].lower() == "true"

    ultimo_periodo = Periodo.objects.filter(parada__zona= zona_id, fin__isnull=True).last()

    if ultimo_periodo != None:
        # Cerramos el periodo anteior
        ultimo_periodo.fin = fecha_dt
        ultimo_periodo.save()  

        ultima_parada_id = ultimo_periodo.parada.id
        ultima_parada = Parada.objects.get(id=ultima_parada_id)
        zona = Zona.objects.get(id=zona_id)

        # Maquina de estados
        if ultima_parada.codigo.siglas == 'RUN': # Desde RUN
            if velocidad > 0.0: # RUN a RUN: Cambio de velocidad, crear un nuevo periodo en la ultima parada
                parada=ultima_parada
            else: 
                if velocidad < 0.0: # RUN a NO_PLC
                    codigo = CodigoParada.objects.filter(siglas='NO_PLC').first()
                else: 
                    if tnp: #RUN a TNP
                        codigo = CodigoParada.objects.filter(siglas='TNP').first()
                    else: # RUN a TNP
                        codigo = CodigoParada.objects.filter(siglas='UNKNOWN').first()
                parada = Parada.objects.create(codigo=codigo, zona=zona)

        elif ultima_parada.codigo.siglas == 'TNP': # Desde TNP
            if velocidad > 0.0: # TNP a RUN
                codigo = CodigoParada.objects.filter(siglas='RUN').first()
                parada = Parada.objects.create(codigo=codigo, zona=zona)
            else:
                if velocidad < 0.0: # TNP a NO_PLC
                    codigo = CodigoParada.objects.filter(siglas='NO_PLC').first()
                    parada = Parada.objects.create(codigo=codigo, zona=zona)
                else: 
                    if tnp: # TNP a TNP
                        parada = ultima_parada
                    else: # TNP a UNKNOWN
                        codigo = CodigoParada.objects.filter(siglas='UNKNOWN').first()  
                        parada = Parada.objects.create(codigo=codigo, zona=zona)

        elif ultima_parada.codigo.siglas == 'UNKNOWN': # Desde UNKNOWN
            if velocidad > 0.0: # UNKNOWN a RUN
                codigo = CodigoParada.objects.filter(siglas='RUN').first()
                parada = Parada.objects.create(codigo=codigo, zona=zona)
            else:
                if velocidad < 0.0: # UNKNOWN a NO_PLC
                    codigo = CodigoParada.objects.filter(siglas='NO_PLC').first()
                    parada = Parada.objects.create(codigo=codigo, zona=zona)
                else: 
                    if tnp: # UNKNOWN a TNP
                        codigo = CodigoParada.objects.filter(siglas='TNP').first()  
                        parada = Parada.objects.create(codigo=codigo, zona=zona)
                    else: # TNP a UNKNOWN
                        parada = ultima_parada
        
        else: # Cualquier otro tipo por implementar
            if velocidad > 0.0: # RUN
                codigo = CodigoParada.objects.filter(siglas='RUN').first()
            else:
                if velocidad < 0.0: # NO_PLC
                    codigo = CodigoParada.objects.filter(siglas='NO_PLC').first()
                else: # UNKNOWN o TNP
                    if tnp:
                        codigo = CodigoParada.objects.filter(siglas='TNP').first()
                    else:
                        codigo = CodigoParada.objects.filter(siglas='UNKNOWN').first()
            parada = Parada.objects.create(codigo=codigo, zona=zona)
                        

    else: # Si no hay ultima parada
        if velocidad > 0.0: # RUN
            codigo = CodigoParada.objects.filter(siglas='RUN').first()
        else:
            if velocidad < 0.0: # NO_PLC
                codigo = CodigoParada.objects.filter(siglas='NO_PLC').first()
            else: # UNKNOWN o TNP
                if tnp:
                    codigo = CodigoParada.objects.filter(siglas='TNP').first()
                else:
                    codigo = CodigoParada.objects.filter(siglas='UNKNOWN').first()
        parada = Parada.objects.create(codigo=codigo, zona=zona)

    periodo = Periodo.objects.create(parada=parada, inicio=fecha_dt, velocidad=velocidad)

    return JsonResponse({"status": "created", "fecha": fecha_str}, status=201)

@api_view(["POST"])
def generar_anual(request):
    year = request.data.get('year')
    if not year:
        return Response({"error": "Falta el año"}, status=400)
    try:
        year=int(year)
        generar_horario_anual(year)
        return Response({"ok": True, "mensaje": "Horarios generados para el año {year} para todas las máquinas"})
    except ValueError:
        return Response({"error": "El año no es válido"}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["GET"])
def obtener_anual(request):
    zona_id = request.GET.get('zona')
    #ano = request.GET.get('ano') si queremos que sea una petición del frontend
    queryset = HorarioDia.objects.all().order_by("fecha")
    if not zona_id:
        return Response({"error": "Falta parámetro zona"}, status=400)
    
    ano_actual = date.today().year #SOLO MUESTRA EL AÑO ACTUAL
    queryset = HorarioDia.objects.filter(zona_id=zona_id, fecha__year=ano_actual).order_by("fecha")
    
    """ queryset = HorarioDia.objects.filter(zona_id=zona_id) ---------> PARA QUE FILTRE LA PETICIÓN DEL FRONTEND
    if ano:
        queryset = queryset.filter(fecha__year=ano)
    queryset = queryset.order_by("fecha") """

    data = [
        {
            "fecha": d.fecha.strftime('%Y-%m-%d'),
            "nombreDia": d.nombre_dia,
            "inicio": str(d.inicio),
            "fin": str(d.fin),
            "es_festivo": d.es_festivo,
            "zona": d.zona.id,
            "zona_siglas": d.zona.siglas, 
            "mes": d.fecha.month,
            "dia": d.fecha.day,
            "anio": d.fecha.year,
            "turno_mañana": d.turno_mañana.id if d.turno_mañana else None,
            "turno_tarde": d.turno_tarde.id if d.turno_tarde else None,
            "turno_noche": d.turno_noche.id if d.turno_noche else None,
            "cambio_turno_1": d.cambio_turno_1,
            "cambio_turno_2": d.cambio_turno_2,
            "semana": d.semana(),
            "id": d.id,
        }
        for d in queryset
    ]

    return Response(data)

@api_view(["PUT"])
def actualizar_horario(request, fecha):
    #import datetime

    zona_id = request.data.get('zona_id')
    if not zona_id:
        return Response({"error": "Falta zona_id en el body"}, status=400)
    try:
        dia = HorarioDia.objects.get(fecha=fecha, zona_id=zona_id)
    except HorarioDia.DoesNotExist:
        return Response({"error": "No existe ese día para esa máquina"}, status=404)

    # Obtener los valores como strings
    inicio = request.data.get("inicio", dia.inicio)
    fin = request.data.get("fin", dia.fin)
    turno_mañana = request.data.get("turno_mañana")
    turno_tarde = request.data.get("turno_tarde")
    turno_noche = request.data.get("turno_noche")
    cambio_turno_1 = request.data.get("cambio_turno_1")
    cambio_turno_2 = request.data.get("cambio_turno_2")

    dia.inicio = inicio
    dia.fin = fin
    dia.turno_mañana_id = turno_mañana if turno_mañana else None
    dia.turno_tarde_id = turno_tarde if turno_tarde else None
    dia.turno_noche_id = turno_noche if turno_noche else None
    dia.cambio_turno_1 = cambio_turno_1 if cambio_turno_1 else None
    dia.cambio_turno_2 = cambio_turno_2 if cambio_turno_2 else None
    
    #si hora inicio y fin es 0.0 pondrá es_festivo a true
    dia.es_festivo = (dia.inicio == time(0, 0) and dia.fin == time(0, 0))
    
    dia.save()

    return Response({"ok": True, "mensaje": "Horario actualizado"})

@api_view(["POST"])
def guardar_festivos(request):
    fechas = request.data.get("fechas")
    zona_id = request.data.get("zona_id")

    if not fechas:
        return Response({"error": "No se recibieron fechas"}, status=400)
    if not zona_id:
        return Response({"error": "No se recibió zona_id"}, status=400)

    # Convertimos a objetos datetime
    import datetime
    
    for f in fechas:
        try:
            fecha_obj = datetime.datetime.strptime(f, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": f"Formato de fecha inválido: {f}"}, status=400)

        try:
            dia = HorarioDia.objects.get(fecha=fecha_obj, zona_id=zona_id)
        except HorarioDia.DoesNotExist:
            continue  # Si no existe el día, lo saltamos

        dia.es_festivo = True
        dia.inicio = datetime.time(0, 0)
        dia.fin = datetime.time(0, 0)
        dia.save()

    return Response({"ok": True, "mensaje": "Festivos actualizados"})

@api_view(["GET"])
def obtener_codigos(request):
    zona_id = request.GET.get('zona')
    tipo_parada = request.GET.get('tipo_parada')
    palabra_clave = request.GET.get('palabra_clave')

    """ if ( type(palabra_clave) != int):
        palabra_clave = 0
    print(f'palabra_clave {palabra_clave}') """

    codigos = CodigoParada.objects.filter(
        Q(palabra_clave = palabra_clave, tipo = tipo_parada, zona = zona_id) |
        Q(palabra_clave = palabra_clave, tipo = tipo_parada, zona__isnull = True) 
    ).distinct().order_by('nombre')

    serializer = CodigoParadaSerializer(codigos, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def obtener_codigos_resto(request):
    zona_id = request.GET.get('zona')
    tipo_parada = request.GET.get('tipo_parada')

    codigos = CodigoParada.objects.filter(
        Q(tipo = tipo_parada, zona = zona_id) |
        Q(tipo = tipo_parada, zona__isnull = True) 
    ).distinct().order_by('nombre')

    serializer = CodigoParadaSerializer(codigos, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def obtener_palabraclave(request):
    zona_id = request.GET.get('zona')

    codigos = PalabrasClave.objects.filter(
        Q(zona=zona_id) |
        Q(zona__isnull = True)
    ).distinct().order_by('nombre')
    
    serializer = PalabrasClaveSerializer(codigos, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def guardar_paradas_agrupadas(request):
    tipo_parada_id = request.data.get("tipo_parada_id")
    codigo_parada_id = request.data.get("codigo_parada_id")
    paradas = request.data.get("paradas")
    observaciones = request.data.get("observaciones")
    tipo_parada = TipoParada.objects.get(id=tipo_parada_id)
    codigo_parada = CodigoParada.objects.get(id=codigo_parada_id)

    tipo_parada = TipoParada.objects.get(id=tipo_parada_id)
    codigo_parada = CodigoParada.objects.get(id=codigo_parada_id)

    # Creamos la lista de todos los IDs seleccionados
    ids = [int(parada['id']) for parada in paradas]

    if tipo_parada.nombre == 'Cambio' and len(ids) > 0:
        primera_id = ids[0]
        # IDs restantes son todos los de la lista menos el primero
        ids_a_eliminar = ids[1:] 
        
        # 1. Actualizamos la parada principal
        Parada.objects.filter(id=primera_id).update(
            codigo=codigo_parada, 
            observaciones=observaciones
        )
        
        # 2. Reasignamos todos los periodos de las otras paradas a la primera
        # Esto evita que los periodos se borren si tienen una relación de Cascada
        Periodo.objects.filter(parada__in=ids).update(parada=primera_id)
        
        # 3. Borramos las paradas que ya no tienen periodos asociados
        if ids_a_eliminar:
            Parada.objects.filter(id__in=ids_a_eliminar).delete()
            
    else:
        # Si no es "Cambio", solo actualizamos la información de todas
        Parada.objects.filter(id__in=ids).update(
            codigo=codigo_parada, 
            observaciones=observaciones
        )

    return Response({"mensaje": "Paradas procesadas y limpieza realizada"}, status=200)

@api_view(["GET"])
def leer_paradas_run(request):
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")
    hora_inicio = request.GET.get("hora_inicio")
    hora_fin = request.GET.get("hora_fin")
    id = request.GET.get("zona")

    inicio_str = f'{fecha_inicio} {hora_inicio}'
    inicio_dt = datetime.strptime(inicio_str, "%Y-%m-%d %H:%M:%S")
    inicio = timezone.make_aware(inicio_dt, timezone.utc)

    fin_str = f'{fecha_fin} {hora_fin}'
    fin_dt = datetime.strptime(fin_str, "%Y-%m-%d %H:%M:%S")
    fin = timezone.make_aware(fin_dt, timezone.utc)

    paradas = Parada.objects.annotate(
        inicio_min=Min('periodos__inicio'),
        fin_max=Max('periodos__fin')
        ).filter(zona=id, codigo__siglas='RUN', inicio_min__gt=inicio, fin_max__lt=fin)
    
    serializer = ParadaSerializer(paradas, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def crear_turnos(request):
    fecha_inicio_turnos = request.data.get("fecha_inicio_turnos")
    fecha_fin_turnos = request.data.get("fecha_fin_turnos")
    zona = request.data.get('zonaId')
    turno_inicio = int(request.data.get('turno_inicio'))
    numero_turnos = int(request.data.get('numero_turnos'))
    hora_cambio_1 = request.data.get('hora_cambio_1')
    hora_cambio_2 = request.data.get('hora_cambio_2')
    if not hora_cambio_1:
        hora_cambio_1 = None
    if not hora_cambio_2:
        hora_cambio_2 = None
    nombre_turno = request.data.get('nombre_turno')

    inicio_date = date.fromisoformat(fecha_inicio_turnos)
    semana_inicio = inicio_date.isocalendar().week
    fin_date = date.fromisoformat(fecha_fin_turnos)
    semana_fin = fin_date.isocalendar().week + 1

    def next_turno(turno_id, nombre_turno, n_turnos):
        print('Calculo next turno ...')
        print(f'numero de turnos {n_turnos} {type(n_turnos)}')
        if n_turnos == 1:
            return turno_id, nombre_turno
        elif n_turnos == 2:
            print('dos turnos ...')
            if nombre_turno == 'A':
                turno = Turnos.objects.filter(zona=zona, activo=True, turno='B').last()
            else:
                turno = Turnos.objects.filter(zona=zona, activo=True, turno='A').last()
            print(f'turno id {turno.id} nombre {turno.turno}')
            if turno:
                return turno.id, turno.turno
            else: 
                return None, None
        elif n_turnos == 3:
            print('tres turnos ...')
            if nombre_turno == 'A':
                turno = Turnos.objects.filter(zona=zona, activo=True, turno='B').last()
            elif nombre_turno == 'B':
                turno = Turnos.objects.filter(zona=zona, activo=True, turno='C').last()
            else:
                turno = Turnos.objects.filter(zona=zona, activo=True, turno='A').last()
            if turno:
                return turno.id, turno.turno
            else: 
                return None, None
        else:
            print('Error en numero de turnos')
            return None, None

    turno_mañana = turno_inicio
    turno_tarde, nonbre = next_turno(turno_mañana, nombre_turno, numero_turnos)
    turno_noche, nombre = next_turno(turno_tarde, nonbre, numero_turnos)
    secuencia = [turno_mañana, turno_tarde, turno_noche]
    
    secuencia = secuencia[:numero_turnos]
    print(secuencia)      

    for week in range(semana_inicio, semana_fin):
        laborables = HorarioDia.objects.filter(
            zona=zona,
            fecha__week=week,
            es_festivo=False,
        )
        if len(laborables) != 0: # Hay días laborables
            print(f'Semana {week} no es festiva')
            print(f'Turno de mañana {secuencia[0]}')
            HorarioDia.objects.filter(
                zona=zona,
                fecha__week=week,
                es_festivo=False,
                fecha__gte=inicio_date,
                fecha__lte=fin_date
            ).update(
                turno_mañana=secuencia[0], 
                turno_tarde=None if len(secuencia) < 2 else secuencia[1],
                turno_noche=None if len(secuencia) < 3 else secuencia[2],
                cambio_turno_1=hora_cambio_1, 
                cambio_turno_2=hora_cambio_2)
            
            # secuencia = secuencia[-1:] + secuencia[:-1]
            secuencia = secuencia[1:] + secuencia[:1]
        else:
            print(f'Semana {week} es festiva')
            HorarioDia.objects.filter(
                zona=zona,
                fecha__week=week,
                fecha__gte=inicio_date,
                fecha__lte=fin_date
            ).update(
                turno_mañana=None, 
                turno_tarde=None,
                turno_noche=None)

    return Response({"mensaje": "Turnos creados ..."}, status=200)

