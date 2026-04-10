from django.core.management.base import BaseCommand
from foso.models import Foso, Linea, Posicion


class Command(BaseCommand):
    help = "Crea las posiciones físicas de las líneas según la geometría del foso"

    def add_arguments(self, parser):
        parser.add_argument(
            '--foso',
            type=int,
            help='ID del foso (opcional). Si no se indica, se crean para todos.'
        )
        parser.add_argument(
            '--linea',
            type=int,
            help='ID de una línea concreta (opcional).'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simula la creación sin guardar nada.'
        )

    def handle(self, *args, **options):
        foso_id = options.get('foso')
        linea_id = options.get('linea')
        dry_run = options.get('dry_run')

        # ─────────────── SELECCIÓN DE LÍNEAS ───────────────
        lineas = Linea.objects.select_related('foso')

        if linea_id:
            lineas = lineas.filter(id=linea_id)
        elif foso_id:
            lineas = lineas.filter(foso_id=foso_id)

        if not lineas.exists():
            self.stdout.write(self.style.WARNING("No se encontraron líneas."))
            return

        total_creadas = 0

        # ─────────────── CREACIÓN DE POSICIONES ───────────────
        for linea in lineas:
            foso = linea.foso
            geometria = foso.columnas_por_altura or {}

            self.stdout.write(
                f"\n📦 Línea '{linea.nombre}' (Foso: {foso.nombre})"
            )

            for altura_str, max_col in geometria.items():
                altura = int(altura_str)

                for columna in range(1, max_col + 1):
                    existe = Posicion.objects.filter(
                        linea=linea,
                        altura=altura,
                        columna=columna
                    ).exists()

                    if existe:
                        continue

                    if not dry_run:
                        Posicion.objects.create(
                            linea=linea,
                            altura=altura,
                            columna=columna
                        )

                    total_creadas += 1
                    self.stdout.write(
                        f"  ➕ Altura {altura}, Columna {columna}"
                        + (" [dry-run]" if dry_run else "")
                    )

        # ─────────────── RESULTADO FINAL ───────────────
        if total_creadas == 0:
            self.stdout.write(self.style.WARNING(
                "\n⚠️  No se creó ninguna posición (ya existían)."
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"\n✅ Posiciones creadas: {total_creadas}"
            ))