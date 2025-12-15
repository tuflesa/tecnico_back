import datetime
from .models import HorarioDia
from estructura.models import Zona

def generar_horario_anual (year):

    inicio = datetime.date(year, 1, 1)
    fin = datetime.date(year, 12, 31)

    nombresDias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    zonas = Zona.objects.filter(es_maquina_tubo=True).exclude(empresa=3) #obtenemos todas las zonas
    print("Zonas encontradas:", zonas)

    delta = datetime.timedelta(days=1)

    #bucle por cada máquina
    for zona in zonas:
        dia = inicio
        while dia <= fin:
            es_festivo = dia.weekday() >= 5
            if es_festivo:
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
                    "es_festivo": es_festivo,
                }
            )
            dia += delta
