import pyodbc
import snap7
from snap7.util import get_fstring, get_int, get_real, get_date, get_time, set_string, set_int, set_real, set_date, set_dint
from datetime import datetime
# import time
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.response import Response
from .models import Acumulador, Flejes, Tubos
from django.db.models import Q

# Constantes
DEBUG = False
ULTIMO_FLEJE = 0
FLEJE_SIZE = 98
TUBO_SIZE = 30
FIFO_POS = 196
FLEJE_ACTUAL = 98
FLEJE_NULO = {
    'pos': 0,
    'idProduccion': '',
    'descripcion': '',
    'peso': 0,
    'of': '',
    'metros_teoricos': 0,
    'IdArticulo': 'F00000001001'
}
TUBO_NULO = {
    'of': '',
    'pos': 0,
    'idProduccion': '',
    'largo': 0,
    'nTubos':0
}

def leerTubosPLC(data, pos):
    tubo = {
        'of': get_fstring(data, pos+2, 8, False),
        'pos': get_int(data, pos+10),
        'idProduccion': get_fstring(data, pos+14, 10, False),
        'largo': get_real(data, pos+24),
        'n_tubos': get_int(data, pos+28)
    }
    return tubo

def leerFlejePLC(data, pos):
    fleje = {
        'of': get_fstring(data, pos+2, 8, False),
        'pos': get_int(data, pos+10),
        'idProduccion': get_fstring(data, pos+14, 10, False),
        'descripcion': get_fstring(data, pos+26, 50, True),
        'peso': get_int(data, pos+76),
        'metros_teoricos': get_real(data, pos+78),
        'metros_medidos': get_real(data, pos+82),
        'fecha_entrada': get_date(data, pos+86),
        'hora_entrada': get_time(data, pos+88),
        'fecha_salida': get_date(data, pos+92),
        'hora_salida': get_time(data, pos+94),
    }
    return fleje

def leerFIFO_FlejePLC(data, pos):
    FIFO = []
    nFlejes = get_int(data, pos)
    for i in range(4):
        FIFO.append(leerFlejePLC(data, pos+2+i*FLEJE_SIZE))

    return nFlejes, FIFO

def metros(fleje):
    # print('calculo metros teoricos')
    # print(fleje)
    espesor = float(fleje['IdArticulo'][9:])/10.0
    ancho = float(fleje['IdArticulo'][6:-3])
    metros = (fleje['peso'] *1000) / (espesor * ancho * 7.85)

    return float(metros)

def reset_tuboPLC(tubo):
    to_PLC = bytearray(TUBO_SIZE)

    set_string(to_PLC, 0, tubo['of'], 8)
    set_int(to_PLC, 10, tubo['pos'])
    set_string(to_PLC, 12, tubo['idProduccion'], 10)
    set_real(to_PLC, 24, tubo['largo'])
    set_int(to_PLC, 28, tubo['nTubos'])

    return to_PLC

def reset_flejePLC(fleje):
    # print(fleje)
    to_PLC = bytearray(FLEJE_SIZE)
    set_string(to_PLC, 0, fleje['of'], 8)
    set_int(to_PLC, 10, fleje['pos'])
    set_string(to_PLC, 12, fleje['idProduccion'], 10)
    set_string(to_PLC, 24, fleje['descripcion'], 50)
    set_int(to_PLC, 76, fleje['peso'])
    set_real(to_PLC, 78, metros(fleje))
    now = datetime.now()
    ms = (now.hour*3600 + now.minute*60 + now.second)*1000 #tiempo desde medianoche en ms
    set_date(to_PLC, 86, now.date())
    set_dint(to_PLC, 88, ms)
    # set_string(to_PLC, 88, now.strftime("%H:%M:%S"),4)
    # set_date(to_PLC, dir+92, None)
    # set_time(to_PLC, dir+94, None)
    return to_PLC

def escribe_flejePLC(fleje):
    # print(fleje)
    to_PLC = bytearray(FLEJE_SIZE)
    set_string(to_PLC, 0, fleje['of'], 8)
    set_int(to_PLC, 10, fleje['pos'])
    set_string(to_PLC, 12, fleje['idProduccion'], 10)
    set_string(to_PLC, 24, fleje['descripcion'], 50)
    set_int(to_PLC, 76, fleje['peso'])
    set_real(to_PLC, 78, fleje['metros_teoricos'])
    return to_PLC

def reset_N_Tubos(N):
    to_PLC = bytearray(2)
    set_int(to_PLC, 0, N)
    return to_PLC

def escribe_N_FIFO(N):
    to_PLC = bytearray(2)
    set_int(to_PLC, 0, N)
    return to_PLC

def actualizarFIFO_PLC(FIFO, nFlejesNuevo, acumulador):
    # print('Actualizar Flejes PLC ...')
    # print(FIFO)
    to_PLC = escribe_N_FIFO(nFlejesNuevo)
    for i in range(nFlejesNuevo):
        to_PLC += escribe_flejePLC(FIFO[i])
    IP = acumulador.ip
    RACK = acumulador.rack
    SLOT = acumulador.slot
    DB = acumulador.db
    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)

    plc.db_write(DB, FIFO_POS, to_PLC)

def leerFlejesProduccionDB():
    consultaSQL = 'select a.xIdPos, a.xIdFleje, a.xIdArticulo, a.xPeso, a.xIdOF, xIdMaquina, art.xdescripcion from imp.tb_tubo_acumulador a inner join imp.tb_tubo_orden o on a.xIdOF = o.xIdOF  left join F126_DATA.imp.pl_articulos art on art.xarticulo_id = a.xIdArticulo WHERE xPesoConsumido = 0 and xTrazabilidad = 0' 
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=10.128.0.203;"
        "DATABASE=Produccion_BD;"
        "UID=reader;"
        "PWD=sololectura;"
        "TrustServerCertificate=yes;"
    )
    datos = []
    try:
        if DEBUG:
            conexion = pyodbc.connect('DRIVER={SQL Server}; SERVER=10.128.0.203;DATABASE=Produccion_BD;UID=reader;PWD=sololectura')
        else:
            conexion = pyodbc.connect(conn_str)
        cursor = conexion.cursor()
        cursor.execute(consultaSQL)
        flejes = cursor.fetchall()
        
        for fleje in flejes:
            f = {
                'pos': fleje[0],
                'idProduccion': fleje[1],
                'IdArticulo': fleje[2],
                'peso': fleje[3],
                'of': fleje[4],
                'maquina_siglas': fleje[5],
                'descripcion': fleje[6]
            }
            datos.append(f)

    except Exception as Ex:
        print(Ex)

    finally:
        conexion.close()

    return datos

@api_view(['POST'])
def leerFlejesEnAcumuladores(request):
    flejes_DB = request.data # Flejes que vienen de la base de datos
    # Para todos los acumuladores vemos si hay algún fleje que no esté ya en el accumulador
    for acc in Acumulador.objects.all():
        print(acc.maquina_siglas)

        if (acc.of_activa):
            # Leemos ProduccionDB y actualizamos el FIFO de flejes
            of_actual = acc.of_activa
        
            flejes_maquina = [f for f in flejes_DB if f['maquina_siglas'] == acc.maquina_siglas] # Filtramos por máquina

            flejes_of_actual = [f for f in flejes_maquina if f['of'] == of_actual]
            flejes_of_actual = sorted(flejes_of_actual, key=lambda f: f['pos']) # Ordenamos por posición

            flejes_of_siguiente = [f for f in flejes_maquina if f['of'] != of_actual]
            flejes_of_siguiente = sorted(flejes_of_siguiente, key=lambda f: f['pos']) # Ordenamos por posición

            # Cambio de of
            if len(flejes_of_actual) == 0 and len(flejes_of_siguiente)>0:
                next_of = flejes_of_siguiente[0]['of']
                flejes_of_siguiente = [f for f in flejes_of_siguiente if f['of'] == next_of]
                flejes_ordenados = flejes_of_siguiente
                add = True
            else: 
                flejes_ordenados = flejes_of_actual
                add = False

            # Comprobar que no hay cambios en el orden de las bobinas leidas
            # Si hay errores, borrar las bobinas a partir de la última que está bien y actualizar PLC si es necesario
            fl = Flejes.objects.filter(of=of_actual, finalizada=False)
            print('numero de flejes no consumidos ', len(fl))
            orden_flejes_OK = True
            for fleje in fl:
                pos = fleje.pos
                flejeDB = list(filter(lambda f: f['pos'] == pos, flejes_of_actual))
                if len(flejeDB)>0:
                    if fleje.idProduccion != flejeDB[0]['idProduccion']: # No coincide el orden
                        print('Cambio de orden de los flejes ...')
                        Flejes.objects.filter(of=of_actual, finalizada=False, pos__gte=pos).delete()
                        acc.n_bobina_ultima = pos - 1
                        acc.save()
                        orden_flejes_OK = False
                        break # Sale del bucle for
                else: # El fleje se ha borrado de producción DB
                    if len(fl)>1 and fleje.pos > acc.n_bobina_activa:
                        print('Fleje borrado de produccion DB...')
                        Flejes.objects.filter(of=of_actual, finalizada=False, pos__gte=pos).delete()
                        acc.n_bobina_ultima = pos - 1
                        acc.save()
                        orden_flejes_OK = False
                        break # Sale del bucle for
            
            # Añadir flejes nuevos
            flejes_a_guardar = []
            for fleje in flejes_ordenados:
                fl = Flejes.objects.filter(pos=fleje['pos'], idProduccion=fleje['idProduccion']).last()
                if (fl == None):
                    flejes_a_guardar.append(fleje) 

            # Guardar flejes nuevos en la base de datos de Técnico
            for fleje in flejes_a_guardar:
                # print(fleje)
                f = Flejes(pos=fleje['pos'], idProduccion=fleje['idProduccion'], IdArticulo=fleje['IdArticulo'],
                           peso=fleje['peso'], of=fleje['of'], maquina_siglas=fleje['maquina_siglas'],
                           descripcion=fleje['descripcion'], acumulador=acc)
                f.save()

            # Actualizar acumulador con la última bobina leida
            if len(flejes_a_guardar)>0:
                acc.n_bobina_ultima=flejes_a_guardar[-1]['pos']
                acc.save()
            else: print('No hay flejes que guardar ...')

            # Leemos el estado del PLC. 
            # Si ha terminado la bobina actual, actualizamos acumulaodor y FIFO de flejes
            # Si no ha terminado actualizamos el estado del fleje actual
            # Si hay nuevas bobinas en el FIFO de bobinas, actualizamos PLC
            if (acc.ip):
                IP = acc.ip
                RACK = acc.rack
                SLOT = acc.slot
                DB = acc.db
                plc = snap7.client.Client()
                plc.connect(IP, RACK, SLOT)

                from_PLC = plc.db_read(DB,0,775)
                ultimo_flejePLC = leerFlejePLC(from_PLC,ULTIMO_FLEJE)
                fleje_ActualPLC = leerFlejePLC(from_PLC,FLEJE_ACTUAL)
                # Leer ultimo tubo del PLC
                ultimo_tubo = leerTubosPLC(from_PLC, 590)
                tubo_actual = leerTubosPLC(from_PLC, 620)

                last_t = Tubos.objects.filter(fleje__acumulador__id=acc.id).order_by('id').last()
                if last_t == None:
                    print('No hay tubos ...')
                    fl = Flejes.objects.filter(of=ultimo_tubo['of'], pos=ultimo_tubo['pos'], idProduccion=ultimo_tubo['idProduccion']).last()
                    if fl != None:
                        new_t = Tubos(n_tubos=ultimo_tubo['n_tubos'] , largo=ultimo_tubo['largo'], fleje= fl)
                        new_t.save()
                    fl = Flejes.objects.filter(of=tubo_actual['of'], pos=tubo_actual['pos'], idProduccion=tubo_actual['idProduccion']).last()
                    if fl != None:
                        new_t = Tubos(n_tubos=tubo_actual['n_tubos'] , largo=tubo_actual['largo'], fleje= fl)
                        new_t.save()
                else:
                    print('Hay tubos')
                    print('last_t', last_t.largo)
                    if (last_t.fleje.of == ultimo_tubo['of'] and last_t.fleje.pos == ultimo_tubo['pos']
                        and last_t.fleje.idProduccion == ultimo_tubo['idProduccion'] and last_t.largo == ultimo_tubo['largo']):
                        print('actualizar ultimo tubo y crear uno nuevo')
                        last_t.n_tubos = ultimo_tubo['n_tubos']
                        last_t.save()
                        fl = Flejes.objects.filter(of=tubo_actual['of'], pos=tubo_actual['pos'], idProduccion=tubo_actual['idProduccion']).last()
                        if fl != None:
                            new_t = Tubos(n_tubos=tubo_actual['n_tubos'] , largo=tubo_actual['largo'], fleje= fl)
                            new_t.save()
                    else:
                        print('Actualizar tubo actual')
                        last_t.n_tubos = tubo_actual['n_tubos']
                        last_t.largo = tubo_actual['largo']
                        last_t.save()
                
                flejeActualPLC_valido = False
                if (ultimo_flejePLC['of'] == acc.of_activa and ultimo_flejePLC['pos'] == acc.n_bobina_activa):
                    print('bobina terminada')
                    f = Flejes.objects.get(of=ultimo_flejePLC['of'], pos=ultimo_flejePLC['pos'])
                    f.metros_medido = ultimo_flejePLC['metros_medidos']
                    f.fecha_entrada = ultimo_flejePLC['fecha_entrada']
                    f.hora_entrada = ultimo_flejePLC['hora_entrada']
                    f.fecha_salida = ultimo_flejePLC['fecha_salida']
                    f.hora_salida = ultimo_flejePLC['hora_salida']
                    f.finalizada = True
                    f.save()
                    acc.of_activa = fleje_ActualPLC['of']
                    acc.n_bobina_activa = fleje_ActualPLC['pos'] 
                    acc.save()
                else:
                    print('Misma bobina')
                    if (fleje_ActualPLC['pos']!=0):
                        print('Actualizar bobina actual')
                        print('of ', fleje_ActualPLC['of'])
                        print('pos ', fleje_ActualPLC['pos'])
                        f = Flejes.objects.get(of=fleje_ActualPLC['of'], pos=fleje_ActualPLC['pos'])
                        f.metros_medido = fleje_ActualPLC['metros_medidos']
                        f.save()
                        flejeActualPLC_valido = True
                    else:
                        print('Fleje actual PLC no valido')

                nFlejesPLC, FIFO_PLC = leerFIFO_FlejePLC(from_PLC, 196)
                if not orden_flejes_OK: # Sobre escribe lo guardado en el PLC para corregir el orden
                    print('Corregir orden en PLC, nFlejes=0')
                    nFlejesPLC = 0
                else:
                    print('Orden de flejes ok ...')
                if (nFlejesPLC<4 and flejeActualPLC_valido):
                    add = False
                    data_to_send = 0
                    for fleje in Flejes.objects.filter(acumulador__id=acc.id ,finalizada = False).order_by('id'):
                        if (add):
                            FIFO_PLC[nFlejesPLC+data_to_send] = {
                                'of': fleje.of,
                                'pos': fleje.pos,
                                'idProduccion': fleje.idProduccion,
                                'IdArticulo': fleje.IdArticulo,
                                'descripcion': fleje.descripcion,
                                'peso': fleje.peso,
                                'metros_teoricos': fleje.metros_teorico()
                            }
                            data_to_send += 1
                            if (data_to_send+nFlejesPLC)==4:
                                add = False
                        if (fleje.pos == fleje_ActualPLC['pos'] and nFlejesPLC==0):
                            add = True
                        if (nFlejesPLC != 0 and fleje.pos == FIFO_PLC[nFlejesPLC-1]['pos']):
                            add = True
                    
                    if (data_to_send >0): 
                        # print('data_to_send', data_to_send)
                        # print('nFlejesPLC', nFlejesPLC)
                        # print('Datos para actualizar FIFO')
                        # print(FIFO_PLC)
                        actualizarFIFO_PLC(FIFO_PLC, nFlejesPLC + data_to_send, acc)
                    
            else:
                print('No hay configuración de la conexión al PLC')

        else: print('No hay bobina activa')


    return HttpResponse(status=201)

@api_view(['POST'])
def resetPLC(request):
    fleje = request.data
    tubo1 = {
        'of': fleje['of'],
        'pos': fleje['pos'],
        'idProduccion': fleje['idProduccion'],
        'largo': 0,
        'nTubos':0
    }
    tubo2 = {
        'of': fleje['of'],
        'pos': fleje['pos'],
        'idProduccion': fleje['idProduccion'],
        'largo': 6000.0,
        'nTubos':0
    }
    acumulador = Acumulador.objects.get(pk = fleje['acumulador'])

    # Borramos todos los flejes no finalizados
    Flejes.objects.filter(acumulador=acumulador.id, finalizada=False).delete()

    # Guarda el fleje seleccionado en la tabla de Flejes
    fl = Flejes.objects.filter(pos=fleje['pos'], idProduccion=fleje['idProduccion']).last()
    if (fl == None): # Si no existe lo crea
        fl = Flejes(pos=fleje['pos'], idProduccion=fleje['idProduccion'], IdArticulo=fleje['IdArticulo'],
                        peso=fleje['peso'], of=fleje['of'], maquina_siglas=fleje['maquina_siglas'],
                        descripcion=fleje['descripcion'], acumulador=acumulador)
        fl.save()
    else: #Si existe, lo actualiza
        fl.finalizada = False
        fl.save()

    # Borra todos los flejes de esa máquina y of con posición mayor que la seleccionada
    Flejes.objects.filter(acumulador=acumulador.id, of=fleje['of'], pos__gt=fleje['pos']).delete()

    # Creamos un tubo de fleje actual con 0 tubos
    Tubos.objects.filter(fleje__pos=fleje['pos'], fleje__idProduccion=fleje['idProduccion']).delete()
    t = Tubos(fleje=fl, largo=6000.0, n_tubos=0)
    t.save()

    # Actualiza el acumulador
    acumulador.of_activa = fleje['of']
    acumulador.n_bobina_activa = fleje['pos']
    acumulador.n_bobina_ultima = fleje['pos']
    acumulador.save()

    # Reseteamos Flejes PLC
    IP = acumulador.ip
    RACK = acumulador.rack
    SLOT = acumulador.slot
    DB = acumulador.db
    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)

    to_PLC = reset_flejePLC(FLEJE_NULO)
    to_PLC += reset_flejePLC(fleje)
    to_PLC += escribe_N_FIFO(0)
    for i in range(1,5):
        to_PLC += reset_flejePLC(FLEJE_NULO)

    to_PLC += reset_tuboPLC(tubo1) # Ultimo tubo
    to_PLC += reset_tuboPLC(tubo2) # Tubo actual
    to_PLC += reset_N_Tubos(0) # N tubos en fifo
    for i in range(1,5):
        to_PLC += reset_tuboPLC(TUBO_NULO)

    plc.db_write(DB, ULTIMO_FLEJE, to_PLC)

    data = {
        'id': fleje['acumulador'],
        'nombre': acumulador.nombre,
        'zona': acumulador.zona.id,
        'maquina_siglas': acumulador.maquina_siglas,
        'of_activa': acumulador.of_activa,
        'n_bobina_activa': acumulador.n_bobina_activa,
        'n_bobina_ultima': acumulador.n_bobina_ultima,
        'ip': acumulador.ip,
        'rack': acumulador.rack,
        'slot': acumulador.slot,
        'db': acumulador.db
    }

    return Response(data) # HttpResponse(status=201)

@api_view(['GET'])
def leerEstadoPLC(request):
    datos = []

    acu_id = request.GET.get('acu_id')
    acumulador = Acumulador.objects.get(id=acu_id)

    if (acumulador.ip):
        IP = acumulador.ip
        RACK = acumulador.rack
        SLOT = acumulador.slot
        DB = acumulador.db

        plc = snap7.client.Client()
        plc.connect(IP, RACK, SLOT)

        from_PLC = plc.db_read(DB,0,589)
        ultimo_fleje = leerFlejePLC(from_PLC,0)
        fleje_actual = leerFlejePLC(from_PLC,98)
        nFlejesPLC, FIFO_PLC = leerFIFO_FlejePLC(from_PLC, 196)
        plc_status = {
            'ultimo_fleje': ultimo_fleje,
            'fleje_actual': fleje_actual,
            'nFlejesFIFO': nFlejesPLC,
            'fifo': FIFO_PLC
            
        }
    else:
        plc_status = {}

    return Response(plc_status)