import snap7
from snap7.util import set_dint
import struct
from rest_framework.decorators import api_view
from rest_framework.response import Response

# QS mtt2
IP = '10.128.1.140'
RACK = 0
SLOT = 1

def get_real(_bytearray, byte_index):
    data = _bytearray[byte_index:byte_index + 4]
    data_real = struct.unpack('>f', struct.pack('4B', *data))[0]
    return data_real

def get_dword(_bytearray, byte_index):
    data = _bytearray[byte_index:byte_index + 4]
    # dword = struct.unpack('>I', struct.pack('4B', *data))[0]
    dword = int.from_bytes(data, 'big')
    return dword

def get_ejes():
    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)


    from_PLC = plc.db_read(46,0,200)
    # Break down
    bd1_inf = get_real(from_PLC,0)
    bd1_sup = get_real(from_PLC,4)
    bd2_inf = get_real(from_PLC,8)
    bd2_sup = get_real(from_PLC,12)

    #IS
    is1_alto = get_real(from_PLC, 156)
    is1_ancho = get_real(from_PLC,160)
    is2_alto = get_real(from_PLC, 164)
    is2_ancho = get_real(from_PLC,168)
    is3_alto = get_real(from_PLC, 172)
    is3_ancho = get_real(from_PLC,176)

    # Lineal
    l_entrada_altura = get_real(from_PLC,16)
    l_entrada_ancho = get_real(from_PLC,20)
    l_entrada_superior = get_real(from_PLC, 24)
    l_salida_altura = get_real(from_PLC,28)
    l_salida_ancho = get_real(from_PLC,32)
    l_salida_superior = get_real(from_PLC, 36)
    l_rod_inf_entrada = get_real(from_PLC, 144)
    l_rod_inf_centro = get_real(from_PLC, 148)
    l_rod_inf_salida = get_real(from_PLC, 152)

    # Fin pass
    fp1_inf = get_real(from_PLC,40)
    fp1_sup = get_real(from_PLC,44)
    fp2_inf = get_real(from_PLC,48)
    fp2_sup = get_real(from_PLC,52)
    fp3_inf = get_real(from_PLC,56)
    fp3_sup = get_real(from_PLC,60)

    # Welding
    w_lat_operador = get_real(from_PLC,64)
    w_lat_motor = get_real(from_PLC,68)
    w_inferior = get_real(from_PLC,72)
    w_cabezal = get_real(from_PLC,180)
    w_sup_alto_op = get_real(from_PLC,184)
    w_sup_alto_mot = get_real(from_PLC,188)
    w_sup_ancho_op = get_real(from_PLC,192)
    w_sup_ancho_mot = get_real(from_PLC,196)

    # Sizing
    ss1_operador = get_real(from_PLC,76)
    ss1_motor = get_real(from_PLC,80)
    ss1_inferior = get_real(from_PLC,84)
    ss1_superior = get_real(from_PLC,88)

    ss2_operador = get_real(from_PLC,92)
    ss2_motor = get_real(from_PLC,96)
    ss2_inferior = get_real(from_PLC,100)
    ss2_superior = get_real(from_PLC,104)

    ss3_operador = get_real(from_PLC,108)
    ss3_motor = get_real(from_PLC,112)
    ss3_inferior = get_real(from_PLC,116)
    ss3_superior = get_real(from_PLC,120)

    ss4_operador = get_real(from_PLC,124)
    ss4_motor = get_real(from_PLC,128)
    ss4_inferior = get_real(from_PLC,132)
    ss4_superior = get_real(from_PLC,136)

    ejes = [{'op': 1, 'pos': {'INF': bd1_inf, 'SUP': bd1_sup}}, 
            {'op': 2, 'pos': {'INF':bd2_inf, 'SUP': bd2_sup}},
            {'op': 3, 'pos': {'ALTO_S1':is1_alto, 'ANCHO_S1': is1_ancho}},
            {'op': 4, 'pos': {'IN_ALTO': l_entrada_altura, 'IN_ANCHO': l_entrada_ancho, 'IN_SUP': l_entrada_superior, 
                              'OUT_ALTO': l_salida_altura, 'OUT_ANCHO': l_salida_ancho, 'OUT_SUP': l_salida_superior,
                              'ROD_INF_IN': l_rod_inf_entrada, 'ROD_INF_CENTRO': l_rod_inf_centro, 'ROD_INF_SAL': l_rod_inf_salida}},
            {'op': 5, 'pos': {'INF': fp1_inf, 'SUP': fp1_sup}},
            {'op': 6, 'pos': {'ALTO':is2_alto, 'ANCHO': is2_ancho}},
            {'op': 7, 'pos': {'INF': fp2_inf, 'SUP': fp2_sup}},
            {'op': 8, 'pos': {'ALTO':is3_alto, 'ANCHO': is3_ancho}},
            {'op': 9, 'pos': {'INF': fp3_inf, 'SUP': fp3_sup}},
            {'op': 10, 'pos': {'LAT_OP': w_lat_operador, 'LAT_MO': w_lat_motor, 'INF_W': w_inferior, 
                              'CAB': w_cabezal, 'SUP_V_OP': w_sup_alto_op, 'SUP_V_MO': w_sup_alto_mot,
                              'SUP_H_OP': w_sup_ancho_op, 'SUP_H_MO': w_sup_ancho_mot}},
            {'op': 11, 'pos': {'INF': ss1_inferior, 'SUP': ss1_superior, 'LAT_OP': ss1_operador, 'LAT_MO': ss1_motor}},                 
            {'op': 12, 'pos': {'INF': ss2_inferior, 'SUP': ss2_superior, 'LAT_OP': ss2_operador, 'LAT_MO': ss2_motor}},
            {'op': 13, 'pos': {'INF': ss3_inferior, 'SUP': ss3_superior, 'LAT_OP': ss3_operador, 'LAT_MO': ss3_motor}},
            {'op': 14, 'pos': {'INF': ss4_inferior, 'SUP': ss4_superior, 'LAT_OP': ss4_operador, 'LAT_MO': ss4_motor}}]

    return ejes

def get_diametros_actuales_PLC():
    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)

    from_PLC = plc.db_read(46,560,140) # 140 Bytes = 35 variables de 4 bytes cada una

    # Pinch Roll
    pinch_roll = get_real(from_PLC,0)
    # Break down
    bd1_inf = get_real(from_PLC,4)
    bd1_sup = get_real(from_PLC,8)
    bd2_inf = get_real(from_PLC,12)
    bd2_sup = get_real(from_PLC,16)
    is1_ancho = get_real(from_PLC,20)
    # Fin pass
    fp1_inf = get_real(from_PLC, 24)
    fp1_sup = get_real(from_PLC, 28)
    fp2_inf = get_real(from_PLC, 32)
    fp2_sup = get_real(from_PLC, 36)
    fp3_inf = get_real(from_PLC, 40)
    fp3_sup = get_real(from_PLC, 44)
    # Welding
    w_inf = get_real(from_PLC, 48)
    w_lat_op = get_real(from_PLC, 52)
    w_lat_mo = get_real(from_PLC, 56)
    w_sup_op = get_real(from_PLC,60)
    w_sup_mo = get_real(from_PLC, 64)
    # Calibradora
    cb1_inf = get_real(from_PLC, 68)
    cb1_sup = get_real(from_PLC, 72)
    cb1_lat_op = get_real(from_PLC, 76)
    cb1_lat_mo = get_real(from_PLC, 80)
    cb2_inf = get_real(from_PLC, 84)
    cb2_sup = get_real(from_PLC, 88)
    cb2_lat_op = get_real(from_PLC, 92)
    cb2_lat_mo = get_real(from_PLC, 96)
    cb3_inf = get_real(from_PLC, 100)
    cb3_sup = get_real(from_PLC, 104)
    cb3_lat_op = get_real(from_PLC, 108)
    cb3_lat_mo = get_real(from_PLC, 112)
    cb4_inf = get_real(from_PLC, 116)
    cb4_sup = get_real(from_PLC, 120)
    cb4_lat_op = get_real(from_PLC, 124)
    cb4_lat_mo = get_real(from_PLC, 128)
    # IS2 IS3
    is2_ancho = get_real(from_PLC,132)
    is3_ancho = get_real(from_PLC,136)

    diametros_actuales ={'BD1': {'INF': bd1_inf, 'SUP': bd1_sup},
                         'BD2': {'INF': bd2_inf, 'SUP': bd2_sup},
                         'IS1': {'ANCHO': is1_ancho, 'ALTO': 0},
                         'FP1': {'INF': fp1_inf, 'SUP': fp1_sup},
                         'IS2': {'ANCHO': is2_ancho, 'ALTO': 0},
                         'FP2': {'INF': fp2_inf, 'SUP': fp2_sup},
                         'IS3': {'ANCHO': is3_ancho, 'ALTO': 0},
                         'FP3': {'INF': fp3_inf, 'SUP': fp3_sup},
                         'W': {'INF': w_inf, 'LAT_OP': w_lat_op, 'LAT_MO': w_lat_mo, 'SUP_OP': w_sup_op, 'SUP_MO': w_sup_mo},
                         'CB1': {'INF': cb1_inf, 'SUP': cb1_sup, 'LAT_OP': cb1_lat_op, 'LAT_MO': cb1_lat_mo},
                         'CB2': {'INF': cb2_inf, 'SUP': cb2_sup, 'LAT_OP': cb2_lat_op, 'LAT_MO': cb2_lat_mo},
                         'CB3': {'INF': cb3_inf, 'SUP': cb3_sup, 'LAT_OP': cb3_lat_op, 'LAT_MO': cb3_lat_mo},
                         'CB4': {'INF': cb4_inf, 'SUP': cb4_sup, 'LAT_OP': cb4_lat_op, 'LAT_MO': cb4_lat_mo}
                         }
    return diametros_actuales

def get_posiciones_actuales_PLC():
    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)

    from_PLC = plc.db_read(46,280,204) # Inicio en la posición 280 - 204 Bytes = 51 variables de 4 bytes cada una

    # Pinch Roll
    pinch_roll_inf = get_real(from_PLC,140) # Siguiente lineal rodillos inferiores
    pinch_roll_press = get_real(from_PLC,200)
    # Break down
    bd1_inf = get_real(from_PLC,0)
    bd1_sup = get_real(from_PLC,4)
    bd2_inf = get_real(from_PLC,8)
    bd2_sup = get_real(from_PLC,12)
    is1_alto = get_real(from_PLC,156)
    is1_ancho = get_real(from_PLC,160) #Siguiente IS2
    # Lineal
    lineal_entrada_altura = get_real(from_PLC,16)
    lineal_entrada_ancho = get_real(from_PLC, 20)
    lineal_entrada_superior = get_real(from_PLC,24)
    lineal_salida_altura = get_real(from_PLC,28)
    lineal_salida_ancho = get_real(from_PLC, 32)
    lineal_salida_superior = get_real(from_PLC,36)
    lineal_rod_inf_entrada = get_real(from_PLC,144) 
    lineal_rod_inf_central = get_real(from_PLC,148)
    lineal_rod_inf_salida = get_real(from_PLC,152) #Siguiente IS1
    # Finpass
    fp1_inf = get_real(from_PLC,40)
    fp1_sup = get_real(from_PLC,44)
    is2_alto = get_real(from_PLC,164)
    is2_ancho = get_real(from_PLC,168) #Siguiente IS3
    fp2_inf = get_real(from_PLC,48)
    fp2_sup = get_real(from_PLC,52)
    is3_alto = get_real(from_PLC,172)
    is3_ancho = get_real(from_PLC,176) #siguiente soldadura cabezal
    fp3_inf = get_real(from_PLC,56)
    fp3_sup = get_real(from_PLC,60)
    # Welding
    w_lat_operador = get_real(from_PLC,64)
    w_lat_motor = get_real(from_PLC,68)
    w_inf = get_real(from_PLC,72)
    w_cabezal = get_real(from_PLC,180)
    w_sup_alto_operador = get_real(from_PLC,184)
    w_sup_alto_motor = get_real(from_PLC,188)
    w_sup_ancho_operador = get_real(from_PLC,192)
    w_sup_ancho_motor = get_real(from_PLC,196) #Ultimo
    # Calibradora
    cb1_lat_operador = get_real(from_PLC,76)
    cb1_lat_motor = get_real(from_PLC,80)
    cb1_inferior = get_real(from_PLC,84)
    cb1_superior = get_real(from_PLC,88)
    cb2_lat_operador = get_real(from_PLC,92)
    cb2_lat_motor = get_real(from_PLC,96)
    cb2_inferior = get_real(from_PLC,100)
    cb2_superior = get_real(from_PLC,104)
    cb3_lat_operador = get_real(from_PLC,108)
    cb3_lat_motor = get_real(from_PLC,112)
    cb3_inferior = get_real(from_PLC,116)
    cb3_superior = get_real(from_PLC,120)
    cb4_lat_operador = get_real(from_PLC,124)
    cb4_lat_motor = get_real(from_PLC,128)
    cb4_inferior = get_real(from_PLC,132)
    cb4_superior = get_real(from_PLC,136) #Siguiente pinchroll - al inicio

    posiciones_actuales = [{'op': 0, 'nombre': 'PR', 'posiciones': [{'eje': 'INF', 'pos': pinch_roll_inf},{'eje': 'PRES', 'pos': pinch_roll_press} ]},
                           {'op': 1, 'nombre': 'BD1', 'posiciones': [{'eje': 'INF', 'pos': bd1_inf},{'eje': 'SUP', 'pos': bd1_sup}]},
                           {'op': 2, 'nombre': 'BD2', 'posiciones': [{'eje': 'INF', 'pos': bd2_inf}, {'eje': 'SUP', 'pos': bd2_sup}]},
                           {'op': 3, 'nombre': 'IS1', 'posiciones': [{'eje': 'ANCHO', 'pos': is1_ancho}, {'eje': 'ALTO', 'pos': is1_alto}]},
                           {'op': 4, 'nombre':'LINEAL', 'posiciones': [{'eje': 'ENTRADA_ALTO', 'pos': lineal_entrada_altura}, {'eje': 'ENTRADA_ANCHO', 'pos': lineal_entrada_ancho}, {'eje': 'ENTRADA_SUP', 'pos': lineal_entrada_superior},
                                                                 {'eje': 'SALIDA_ALTO','pos': lineal_salida_altura}, {'eje': 'SALIDA_ANCHO', 'pos': lineal_salida_ancho}, {'eje': 'SALIDA_SUP', 'pos': lineal_salida_superior},
                                                                 { 'eje': 'RODILLO_INF_ENTRADA', 'pos': lineal_rod_inf_entrada}, {'eje': 'RODILLO_INF_CENTRO', 'pos': lineal_rod_inf_central}, {'eje': 'RODILLO_INF_SALIDA', 'pos': lineal_rod_inf_salida}]},
                            {'op': 5, 'nombre': 'FP1', 'posiciones': [{'eje': 'INF', 'pos': fp1_inf}, {'eje': 'SUP', 'pos': fp1_sup}]},
                            {'op': 6, 'nombre': 'IS2', 'posiciones': [{'eje': 'ANCHO', 'pos': is2_ancho}, {'eje': 'ALTO', 'pos': is2_alto}]},
                            {'op': 7, 'nombre': 'FP2', 'posiciones': [{'eje': 'INF', 'pos': fp2_inf}, {'eje': 'SUP', 'pos': fp2_sup}]},
                            {'op': 8, 'nombre': 'IS3', 'posiciones': [{'eje': 'ANCHO', 'pos': is3_ancho}, {'eje': 'ALTO', 'pos': is3_alto}]},
                            {'op': 9, 'nombre': 'FP3', 'posiciones': [{'eje': 'INF', 'pos': fp3_inf}, {'eje': 'SUP', 'pos': fp3_sup}]},
                            {'op': 10, 'nombre': 'W', 'posiciones': [{'eje': 'CAB', 'pos': w_cabezal}, {'eje': 'LAT_OP', 'pos': w_lat_operador}, {'eje': 'LAT_MO', 'pos': w_lat_motor}, {'eje': 'INF', 'pos': w_inf},
                                                               {'eje': 'SUP_V_OP', 'pos': w_sup_alto_operador}, {'eje': 'SUP_H_OP', 'pos': w_sup_ancho_operador}, {'eje': 'SUP_V_MO', 'pos': w_sup_alto_motor}, {'eje': 'SUP_H_MO', 'pos': w_sup_ancho_motor}]},
                            {'op': 12, 'nombre': 'CB1', 'posiciones': [{'eje': 'SUP', 'pos': cb1_superior}, {'eje': 'INF', 'pos': cb1_inferior}, {'eje': 'LAT_OP', 'pos': cb1_lat_operador}, {'eje': 'LAT_MO', 'pos': cb1_lat_motor}]},
                            {'op': 13, 'nombre': 'CB2', 'posiciones': [{'eje': 'SUP', 'pos': cb2_superior}, {'eje': 'INF', 'pos': cb2_inferior}, {'eje': 'LAT_OP', 'pos': cb2_lat_operador}, {'eje': 'LAT_MO', 'pos': cb2_lat_motor}]},
                            {'op': 14, 'nombre': 'CB3', 'posiciones': [{'eje': 'SUP', 'pos': cb3_superior}, {'eje': 'INF', 'pos': cb3_inferior}, {'eje': 'LAT_OP', 'pos': cb3_lat_operador}, {'eje': 'LAT_MO', 'pos': cb3_lat_motor}]},
                            {'op': 15, 'nombre': 'CB4', 'posiciones': [{'eje': 'SUP', 'pos': cb4_superior}, {'eje': 'INF', 'pos': cb4_inferior}, {'eje': 'LAT_OP', 'pos': cb4_lat_operador}, {'eje': 'LAT_MO', 'pos': cb4_lat_motor}]},
                            ]
    return posiciones_actuales

def get_PC(): # Lee los datos que se han enviado al PLC - No los datos actuales

    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)


    from_PLC = plc.db_read(60,144,256)

    # Break down 1 & 2
    bd1_sup_w = get_dword(from_PLC,0)/100.0
    bd1_inf_w = get_dword(from_PLC,8)/100.0

    bd2_sup_w = get_dword(from_PLC,16)/100.0
    bd2_inf_w = get_dword(from_PLC,24)/100.0

    # Lineal
    l_in_sup_w = get_dword(from_PLC,32)/100.0
    l_out_sup_w = get_dword(from_PLC,36)/100.0
    l_in_inf_w = get_dword(from_PLC,40)/100.0
    l_out_inf_w = get_dword(from_PLC,44)/100.0
    l_in_width_w = get_dword(from_PLC,48)/100.0
    l_out_width_w = get_dword(from_PLC,52)/100.0

    # Fin pass
    fp1_sup_w = get_dword(from_PLC,56)/100.0
    fp1_inf_w = get_dword(from_PLC,64)/100.0
    fp2_sup_w = get_dword(from_PLC,72)/100.0
    fp2_inf_w = get_dword(from_PLC,80)/100.0
    fp3_sup_w = get_dword(from_PLC,88)/100.0
    fp3_inf_w = get_dword(from_PLC,96)/100.0

    # welding
    w_inf_w = get_dword(from_PLC,104)/1000.0
    w_op_w = get_dword(from_PLC,112)/1000.0
    w_mot_w = get_dword(from_PLC,120)/1000.0

    pc = [{'op': 1, 'pos': {'INF': bd1_inf_w, 'SUP': bd1_sup_w}}, 
          {'op': 2, 'pos': {'INF':bd2_inf_w, 'SUP': bd2_sup_w}},
          {'op': 3, 'pos': {'IN_ALTO': l_in_inf_w, 'IN_ANCHO': l_in_width_w, 'IN_SUP': l_in_sup_w, 'OUT_ALTO': l_out_inf_w, 'OUT_ANCHO': l_out_width_w, 'OUT_SUP': l_out_sup_w}},
          {'op': 4, 'pos': {'INF': fp1_inf_w, 'SUP': fp1_sup_w}},
          {'op': 5, 'pos': {'INF': fp2_inf_w, 'SUP': fp2_sup_w}},
          {'op': 6, 'pos': {'INF': fp3_inf_w, 'SUP': fp3_sup_w}},
          {'op': 7, 'pos': {'LAT_OP': w_op_w, 'LAT_MO': w_mot_w, 'INF': w_inf_w}}]
    
    return pc

@api_view(['POST'])
def enviarVariantePLC(request):
    variante = request.data
    print(variante)
    pinch_roll_inf = int(variante['pr_inf']*100) # 2 decimales
    pinch_roll_press = int(variante['pr_press']*100) # 2 decimales
    bd1_inf = int(variante['bd1_inf']*100) # 2 decimales
    bd1_sup = int(variante['bd1_sup']*100) # 2 decimales
    bd2_inf = int(variante['bd2_inf']*100) # 2 decimales
    bd2_sup = int(variante['bd2_sup']*100) # 2 decimales
    is1_ancho = int(variante['is1_ancho']*100) # 2 decimales
    is1_alto = int(variante['is1_alto']*100) # 2 decimales
    l_entrada_ancho = int(variante['lineal_entrada_ancho']*100) # 2 decimales
    l_entrada_alto = int(variante['lineal_entrada_alto']*100) # 2 decimales
    l_entrada_sup = int(variante['lineal_entrada_superior']*100) # 2 decimales
    l_salida_ancho = int(variante['lineal_salida_ancho']*100) # 2 decimales
    l_salida_alto = int(variante['lineal_salida_alto']*100) # 2 decimales
    l_salida_sup = int(variante['lineal_salida_superior']*100) # 2 decimales
    l_rod_entrada = int(variante['lineal_rodillo_entrada']*100) # 2 decimales
    l_rod_centro = int(variante['lineal_rodillo_centro']*100) # 2 decimales
    l_rod_salida = int(variante['lineal_rodillo_salida']*100) # 2 decimales
    fp1_inf = int(variante['fp1_inf']*100) # 2 decimales
    fp1_sup = int(variante['fp1_sup']*100) # 2 decimales
    is2_ancho = int(variante['is2_ancho']*100) # 2 decimales
    is2_alto = int(variante['is2_alto']*100) # 2 decimales
    fp2_inf = int(variante['fp2_inf']*100) # 2 decimales
    fp2_sup = int(variante['fp2_sup']*100) # 2 decimales
    is3_ancho = int(variante['is3_ancho']*100) # 2 decimales
    is3_alto = int(variante['is3_alto']*100) # 2 decimales
    fp3_inf = int(variante['fp3_inf']*100) # 2 decimales
    fp3_sup = int(variante['fp3_sup']*100) # 2 decimales
    w_cab = int(variante['w_cab']*1000) # 3 decimales
    w_lat_op = int(variante['w_lat_op']*1000) # 3 decimales
    w_lat_mo = int(variante['w_lat_mo']*1000) # 3 decimales
    w_inf = int(variante['w_inf']*1000) # 3 decimales
    w_sup_v_op = int(variante['w_sup_v_op']*1000) # 3 decimales
    w_sup_v_mo = int(variante['w_sup_v_mo']*1000) # 3 decimales
    w_sup_h_op = int(variante['w_sup_h_op']*1000) # 3 decimales
    w_sup_h_mo = int(variante['w_sup_h_mo']*1000) # 3 decimales
    cb1_sup = int(variante['cb1_sup']*1000) # 3 decimales
    cb1_inf = int(variante['cb1_inf']*1000) # 3 decimales
    cb1_lat_op = int(variante['cb1_lat_op']*1000) # 3 decimales
    cb1_lat_mo = int(variante['cb1_lat_mo']*1000) # 3 decimales
    cb2_sup = int(variante['cb2_sup']*1000) # 3 decimales
    cb2_inf = int(variante['cb2_inf']*1000) # 3 decimales
    cb2_lat_op = int(variante['cb2_lat_op']*1000) # 3 decimales
    cb2_lat_mo = int(variante['cb2_lat_mo']*1000) # 3 decimales
    cb3_sup = int(variante['cb3_sup']*1000) # 3 decimales
    cb3_inf = int(variante['cb3_inf']*1000) # 3 decimales
    cb3_lat_op = int(variante['cb3_lat_op']*1000) # 3 decimales
    cb3_lat_mo = int(variante['cb3_lat_mo']*1000) # 3 decimales
    cb4_sup = int(variante['cb4_sup']*1000) # 3 decimales
    cb4_inf = int(variante['cb4_inf']*1000) # 3 decimales
    cb4_lat_op = int(variante['cb4_lat_op']*1000) # 3 decimales
    cb4_lat_mo = int(variante['cb4_lat_mo']*1000) # 3 decimales
    # Diametros
    bd1_inf_d = int(variante['BD1_INF_D']*100) # 2 decimales
    bd1_sup_d = int(variante['BD1_SUP_D']*100) # 2 decimales
    bd2_inf_d = int(variante['BD2_INF_D']*100) # 2 decimales
    bd2_sup_d = int(variante['BD2_SUP_D']*100) # 2 decimales
    is1_ancho_d = int(variante['IS1_ANCHO_D']*100) # 2 decimales
    is1_alto_d = int(variante['IS1_ALTO_D']*100) # 2 decimales
    fp1_inf_d = int(variante['FP1_INF_D']*100) # 2 decimales
    fp1_sup_d = int(variante['FP1_SUP_D']*100) # 2 decimales
    is2_ancho_d = int(variante['IS2_ANCHO_D']*100) # 2 decimales
    is2_alto_d = int(variante['IS2_ALTO_D']*100) # 2 decimales
    fp2_inf_d = int(variante['FP2_INF_D']*100) # 2 decimales
    fp2_sup_d = int(variante['FP2_SUP_D']*100) # 2 decimales
    is3_ancho_d = int(variante['IS3_ANCHO_D']*100) # 2 decimales
    is3_alto_d = int(variante['IS3_ALTO_D']*100) # 2 decimales
    fp3_inf_d = int(variante['FP3_INF_D']*100) # 2 decimales
    fp3_sup_d = int(variante['FP3_SUP_D']*100) # 2 decimales
    w_inf_d = int(variante['W_INF_D']*1000) # 3 decimales
    w_lat_op_d = int(variante['W_LAT_OP_D']*1000) # 3 decimales
    w_lat_mo_d = int(variante['W_LAT_MO_D']*1000) # 3 decimales
    w_sup_op_d = int(variante['W_SUP_OP_D']*1000) # 3 decimales
    w_sup_mo_d = int(variante['W_SUP_MO_D']*1000) # 3 decimales
    cb1_sup_d = int(variante['CB1_SUP_D']*1000) # 3 decimales
    cb1_inf_d = int(variante['CB1_INF_D']*1000) # 3 decimales
    cb1_lat_op_d = int(variante['CB1_LAT_OP_D']*1000) # 3 decimales
    cb1_lat_mo_d = int(variante['CB1_LAT_MO_D']*1000) # 3 decimales
    cb2_sup_d = int(variante['CB2_SUP_D']*1000) # 3 decimales
    cb2_inf_d = int(variante['CB2_INF_D']*1000) # 3 decimales
    cb2_lat_op_d = int(variante['CB2_LAT_OP_D']*1000) # 3 decimales
    cb2_lat_mo_d = int(variante['CB2_LAT_MO_D']*1000) # 3 decimales
    cb3_sup_d = int(variante['CB3_SUP_D']*1000) # 3 decimales
    cb3_inf_d = int(variante['CB3_INF_D']*1000) # 3 decimales
    cb3_lat_op_d = int(variante['CB3_LAT_OP_D']*1000) # 3 decimales
    cb3_lat_mo_d = int(variante['CB3_LAT_MO_D']*1000) # 3 decimales
    cb4_sup_d = int(variante['CB4_SUP_D']*1000) # 3 decimales
    cb4_inf_d = int(variante['CB4_INF_D']*1000) # 3 decimales
    cb4_lat_op_d = int(variante['CB4_LAT_OP_D']*1000) # 3 decimales
    cb4_lat_mo_d = int(variante['CB4_LAT_MO_D']*1000) # 3 decimales

    to_PLC = bytearray(356)

    set_dint(to_PLC, 0, 1) # 1 para indicar que hay datos nuevos
    set_dint(to_PLC, 4, pinch_roll_inf)
    set_dint(to_PLC, 8, pinch_roll_press)
    set_dint(to_PLC, 12, bd1_inf)
    set_dint(to_PLC, 16, bd1_sup)
    set_dint(to_PLC, 20, bd2_inf)
    set_dint(to_PLC, 24, bd2_sup)
    set_dint(to_PLC, 28, is1_ancho)
    set_dint(to_PLC, 32, is1_alto)
    set_dint(to_PLC, 36, l_entrada_alto)
    set_dint(to_PLC, 40, l_entrada_ancho)
    set_dint(to_PLC, 44, l_entrada_sup)
    set_dint(to_PLC, 48, l_salida_alto)
    set_dint(to_PLC, 52, l_salida_ancho)
    set_dint(to_PLC, 56, l_salida_sup)
    set_dint(to_PLC, 60, l_rod_entrada)
    set_dint(to_PLC, 64, l_rod_centro)
    set_dint(to_PLC, 68, l_rod_salida)
    set_dint(to_PLC, 72, fp1_inf)
    set_dint(to_PLC, 76, fp1_sup)
    set_dint(to_PLC, 80, is2_ancho)
    set_dint(to_PLC, 84, is2_alto)
    set_dint(to_PLC, 88, fp2_inf)
    set_dint(to_PLC, 92, fp2_sup)
    set_dint(to_PLC, 96, is3_ancho)
    set_dint(to_PLC, 100, is3_alto)
    set_dint(to_PLC, 104, fp3_inf)
    set_dint(to_PLC, 108, fp3_sup)
    set_dint(to_PLC, 112, w_cab)
    set_dint(to_PLC, 116, w_lat_op)
    set_dint(to_PLC, 120, w_lat_mo)
    set_dint(to_PLC, 124, w_inf)
    set_dint(to_PLC, 128, w_sup_v_op)
    set_dint(to_PLC, 132, w_sup_v_mo)
    set_dint(to_PLC, 136, w_sup_h_op)
    set_dint(to_PLC, 140, w_sup_h_mo)
    set_dint(to_PLC, 144, cb1_sup)
    set_dint(to_PLC, 148, cb1_inf)
    set_dint(to_PLC, 152, cb1_lat_op)
    set_dint(to_PLC, 156, cb1_lat_mo)
    set_dint(to_PLC, 160, cb2_sup)
    set_dint(to_PLC, 164, cb2_inf)
    set_dint(to_PLC, 168, cb2_lat_op)
    set_dint(to_PLC, 172, cb2_lat_mo)
    set_dint(to_PLC, 176, cb3_sup)
    set_dint(to_PLC, 180, cb3_inf)
    set_dint(to_PLC, 184, cb3_lat_op)
    set_dint(to_PLC, 188, cb3_lat_mo)
    set_dint(to_PLC, 192, cb4_sup)
    set_dint(to_PLC, 196, cb4_inf)
    set_dint(to_PLC, 200, cb4_lat_op)
    set_dint(to_PLC, 204, cb4_lat_mo)
    # Diametros
    set_dint(to_PLC, 208, bd1_inf_d)
    set_dint(to_PLC, 212, bd1_sup_d)
    set_dint(to_PLC, 216, bd2_inf_d)
    set_dint(to_PLC, 220, bd2_sup_d)
    set_dint(to_PLC, 224, is1_ancho_d)
    set_dint(to_PLC, 228, is1_alto_d)
    set_dint(to_PLC, 232, fp1_inf_d)
    set_dint(to_PLC, 236, fp1_sup_d)
    set_dint(to_PLC, 240, is2_ancho_d)
    set_dint(to_PLC, 244, is2_alto_d)
    set_dint(to_PLC, 248, fp2_inf_d)
    set_dint(to_PLC, 252, fp2_sup_d)
    set_dint(to_PLC, 256, is3_ancho_d)
    set_dint(to_PLC, 260, is3_alto_d)
    set_dint(to_PLC, 264, fp3_inf_d)
    set_dint(to_PLC, 268, fp3_sup_d)
    set_dint(to_PLC, 272, w_inf_d)
    set_dint(to_PLC, 276, w_lat_op_d)
    set_dint(to_PLC, 280, w_lat_mo_d)
    set_dint(to_PLC, 284, w_sup_op_d)
    set_dint(to_PLC, 288, w_sup_mo_d)
    set_dint(to_PLC, 292, cb1_sup_d)
    set_dint(to_PLC, 296, cb1_inf_d)
    set_dint(to_PLC, 300, cb1_lat_op_d)
    set_dint(to_PLC, 304, cb1_lat_mo_d)
    set_dint(to_PLC, 308, cb2_sup_d)
    set_dint(to_PLC, 312, cb2_inf_d)
    set_dint(to_PLC, 316, cb2_lat_op_d)
    set_dint(to_PLC, 320, cb2_lat_mo_d)
    set_dint(to_PLC, 324, cb3_sup_d)
    set_dint(to_PLC, 328, cb3_inf_d)
    set_dint(to_PLC, 332, cb3_lat_op_d)
    set_dint(to_PLC, 336, cb3_lat_mo_d)
    set_dint(to_PLC, 340, cb4_sup_d)
    set_dint(to_PLC, 344, cb4_inf_d)
    set_dint(to_PLC, 348, cb4_lat_op_d)
    set_dint(to_PLC, 352, cb4_lat_mo_d)

    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)

    plc.db_write(46, 700, to_PLC)
    return Response('OK')