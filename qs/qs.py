import snap7
import struct

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

    from_PLC = plc.db_read(46,280,200) # Inicio en la posición 280 - 200 Bytes = 50 variables de 4 bytes cada una

    # Pinch Roll
    pinch_roll_inf = cb3_superior = get_real(from_PLC,140) # Siguiente lineal rodillos inferiores
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

    posiciones_actuales = {'PR':  {'INF': pinch_roll_inf},
                           'BD1': {'INF': bd1_inf, 'SUP': bd1_sup},
                           'BD2': {'INF': bd2_inf, 'SUP': bd2_sup},
                           'IS1': {'ANCHO': is1_ancho, 'ALTO': is1_alto},
                           'LINEAL': {'ENTRADA_ALTO': lineal_entrada_altura, 'ENTRADA_ANCHO': lineal_entrada_ancho, 'ENTRADA_SUP': lineal_entrada_superior,
                                      'SALIDA_ALTO': lineal_salida_altura, 'SALIDA_ANCHO': lineal_salida_ancho, 'SALIDA_SUP': lineal_salida_superior,
                                      'RODILLO_INF_ENTRADA': lineal_rod_inf_entrada, 'RODILLO_INF_CENTRO': lineal_rod_inf_central, 'RODILLO_INF_SALIDA': lineal_rod_inf_salida},
                            'FP1': {'INF': fp1_inf, 'SUP': fp1_sup},
                            'IS2': {'ANCHO': is2_ancho, 'ALTO': is2_alto},
                            'FP2': {'INF': fp2_inf, 'SUP': fp2_sup},
                            'IS3': {'ANCHO': is3_ancho, 'ALTO': is3_alto},
                            'FP3': {'INF': fp3_inf, 'SUP': fp3_sup},
                            'W':   {'CAB': w_cabezal, 'LAT_OP': w_lat_operador, 'LAT_MO': w_lat_motor, 'INF': w_inf,
                                  'SUP_ALTO_OP': w_sup_alto_operador, 'SUP_ANCHO_OP': w_sup_ancho_operador, 'SUP_ALTO_MO': w_sup_alto_motor, 'SUP_ANCHO_MO': w_sup_ancho_motor},
                            'CB1': {'SUP': cb1_superior, 'INF': cb1_inferior, 'LAT_OP': cb1_lat_operador, 'LAT_MO': cb1_lat_motor},
                            'CB2': {'SUP': cb2_superior, 'INF': cb2_inferior, 'LAT_OP': cb2_lat_operador, 'LAT_MO': cb2_lat_motor},
                            'CB3': {'SUP': cb3_superior, 'INF': cb3_inferior, 'LAT_OP': cb3_lat_operador, 'LAT_MO': cb3_lat_motor},
                            'CB4': {'SUP': cb4_superior, 'INF': cb4_inferior, 'LAT_OP': cb4_lat_operador, 'LAT_MO': cb4_lat_motor},
                            }
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