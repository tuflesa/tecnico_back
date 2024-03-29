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

def get_ejes():
    plc = snap7.client.Client()
    plc.connect(IP, RACK, SLOT)


    from_PLC = plc.db_read(46,0,140)
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

    ejes = [{'op': 1, 'pos': {'INF': bd1_inf, 'SUP': bd1_sup}}, 
            {'op': 2, 'pos': {'INF':bd2_inf, 'SUP': bd2_sup}},
            {'op': 3, 'pos': {'IN_ALTO': l_entrada_altura, 'IN_ANCHO': l_entrada_ancho, 'IN_SUP': l_entrada_superior, 'OUT_ALTO': l_salida_altura, 'OUT_ANCHO': l_salida_ancho, 'OUT_SUP': l_salida_superior}},
            {'op': 4, 'pos': {'INF': fp1_inf, 'SUP': fp1_sup}},
            {'op': 5, 'pos': {'INF': fp2_inf, 'SUP': fp2_sup}},
            {'op': 6, 'pos': {'INF': fp3_inf, 'SUP': fp3_sup}},
            {'op': 7, 'pos': {'LAT_OP': w_lat_operador, 'LAT_MO': w_lat_motor, 'INF': w_inferior}}]

    return ejes