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

    # Lineal
    l_entrada_altura = get_real(from_PLC,16)
    l_entrada_ancho = get_real(from_PLC,20)
    l_entrada_superior = get_real(from_PLC, 24)
    l_salida_altura = get_real(from_PLC,28)
    l_salida_ancho = get_real(from_PLC,32)
    l_salida_superior = get_real(from_PLC, 36)

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

    ejes = [{'op': 1, 'pos': {'INF': bd1_inf, 'SUP': bd1_sup}}, 
            {'op': 2, 'pos': {'INF':bd2_inf, 'SUP': bd2_sup}},
            {'op': 3, 'pos': {'IN_ALTO': l_entrada_altura, 'IN_ANCHO': l_entrada_ancho, 'IN_SUP': l_entrada_superior, 'OUT_ALTO': l_salida_altura, 'OUT_ANCHO': l_salida_ancho, 'OUT_SUP': l_salida_superior}},
            {'op': 4, 'pos': {'INF': fp1_inf, 'SUP': fp1_sup}},
            {'op': 5, 'pos': {'INF': fp2_inf, 'SUP': fp2_sup}},
            {'op': 6, 'pos': {'INF': fp3_inf, 'SUP': fp3_sup}},
            {'op': 7, 'pos': {'LAT_OP': w_lat_operador, 'LAT_MO': w_lat_motor, 'INF': w_inferior, 
                              'CAB': w_cabezal, 'SUP_ALTO_OP': w_sup_alto_op, 'SUP_ALTO_MOT': w_sup_alto_mot,
                              'SUP_ANCHO_OP': w_sup_ancho_op, 'SUP_ANCHO_MOT': w_sup_ancho_mot}}]

    return ejes

def get_PC():
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