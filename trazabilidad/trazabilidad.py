import pyodbc
import snap7
from snap7.util import get_fstring, get_int, get_real, get_date, get_time, set_string, set_int, set_real, set_date, set_dint
from datetime import datetime
# import time
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.response import Response
from .models import Acumulador, Flejes

# Constantes
ULTIMO_FLEJE = 0
FLEJE_SIZE = 98
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
    datos = []
    try:
        conexion = pyodbc.connect('DRIVER={SQL Server}; SERVER=10.128.0.203;DATABASE=Produccion_BD;UID=reader;PWD=sololectura')
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

            flejes_ordenados = flejes_of_actual + flejes_of_siguiente

            add = False
            flejes_a_guardar = []
            for fleje in flejes_ordenados:
                if (add):
                    flejes_a_guardar.append(fleje) 
                if ( not add and fleje['pos'] == acc.n_bobina_ultima):
                    add = True

            # print('Flejes a guardar')
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

                from_PLC = plc.db_read(DB,0,889)
                # print('Ultima bobina')
                ultimo_flejePLC = leerFlejePLC(from_PLC,ULTIMO_FLEJE)
                # print(ultimo_flejePLC)
                # print('Bobina actual ...')
                fleje_ActualPLC = leerFlejePLC(from_PLC,FLEJE_ACTUAL)
                # print(fleje_ActualPLC)
                # print('Fleje actual')
                # print(fleje_ActualPLC)
                
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
                    acc.n_bobina_activa = fleje_ActualPLC['pos']
                    acc.of_activa = fleje_ActualPLC['of']
                    acc.save()
                else:
                    print('Misma bobina')
                    if (fleje_ActualPLC['pos']!=0):
                        print('Actualizar bobina actual')
                        f = Flejes.objects.get(of=fleje_ActualPLC['of'], pos=fleje_ActualPLC['pos'])
                        f.metros_medido = fleje_ActualPLC['metros_medidos']
                        f.save()
                        flejeActualPLC_valido = True
                    else:
                        print('Fleje actual PLC no valido')

                nFlejesPLC, FIFO_PLC = leerFIFO_FlejePLC(from_PLC, 196)
                if (nFlejesPLC<4 and flejeActualPLC_valido):
                    add = False
                    data_to_send = 0
                    for fleje in Flejes.objects.filter(finalizada = False).order_by('id'):
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
                            print('Add true')
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
    acumulador = Acumulador.objects.get(pk = fleje['acumulador'])

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

    plc.db_write(DB, ULTIMO_FLEJE, to_PLC)

    return HttpResponse(status=201)

@api_view(['GET'])
def leerEstadoPLC(request):
    datos = []

    acu_id = request.GET.get('acu_id')
    acumulador = Acumulador.objects.get(id=acu_id)
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
    return Response(plc_status)