import datetime
from .models import HorarioDia

def generar_horario_anual():
    hoy = datetime.date.today()
    año = hoy.year

    inicio = datetime.date(año, 1, 1)
    fin = datetime.date(año, 12, 31)

    nombresDias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    delta = datetime.timedelta(days=1)
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
            defaults={
                "nombre_dia": nombresDias[dia.weekday()],
                "inicio": hora_inicio,
                "fin": hora_fin,
                "es_fin_de_semana": es_fin_semana,
            }
        )
        dia += delta
