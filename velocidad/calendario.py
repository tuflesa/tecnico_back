import datetime
from .models import HorarioDia
from estructura.models import Zona

def generar_horario_anual(zona_id=None):
    hoy = datetime.date.today()
    año = hoy.year

    inicio = datetime.date(año, 1, 1)
    fin = datetime.date(año, 12, 31)

    nombresDias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    zonas = Zona.objects.filter(es_maquina_tubo=True).exclude(empresa=3) #obtenemos todas las zonas
    print("Zonas encontradas:", zonas)

    delta = datetime.timedelta(days=1)

    #bucle por cada máquina
    for zona in zonas:
        dia = inicio
        while dia <= fin:
            es_fin_semana = dia.weekday() >= 5
            if es_fin_semana:
                hora_inicio = datetime.time(0, 0)
                hora_fin = datetime.time(0, 0)
            else:
                hora_inicio = datetime.time(6, 0)
                hora_fin = datetime.time(22, 0)

            HorarioDia.objects.get_or_create(
                fecha=dia,
                zona=zona,
                defaults={
                    "nombre_dia": nombresDias[dia.weekday()],
                    "inicio": hora_inicio,
                    "fin": hora_fin,
                    "es_fin_de_semana": es_fin_semana,
                }
            )
            dia += delta
