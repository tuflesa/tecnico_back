from django.core.management.base import BaseCommand
from foso.models import Linea, Posicion

COLUMNAS_POR_ALTURA = {
    1: 9,
    2: 8,
    3: 9,
    4: 8,
    5: 9,
}

class Command(BaseCommand):
    help = "Crea todas las posiciones válidas para las líneas del foso."

    def add_arguments(self, parser):
        parser.add_argument('--linea', type=int, help='ID de una línea concreta')
        parser.add_argument('--todas', action='store_true', help='Crear para todas las líneas activas')

    def handle(self, *args, **options):
        if options['todas']:
            lineas = Linea.objects.filter(activa=True)
        else:
            lineas = Linea.objects.filter(pk=options['linea'])
            if not lineas.exists():
                self.stderr.write(f"Línea {options['linea']} no encontrada.")
                return

        total = 0
        for linea in lineas:
            creadas = 0
            for altura, max_col in COLUMNAS_POR_ALTURA.items():
                for columna in range(1, max_col + 1):
                    _, created = Posicion.objects.get_or_create(
                        linea=linea, altura=altura, columna=columna
                    )
                    if created:
                        creadas += 1
            self.stdout.write(f"  {linea.nombre}: {creadas} posiciones creadas.")
            total += creadas

        self.stdout.write(self.style.SUCCESS(f"Total: {total} posiciones creadas."))