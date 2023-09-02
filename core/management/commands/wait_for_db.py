"""
Comando de Django que espera la base de datos este disponible
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Comando de Django para esperar la base de datos."""

    def handle(self, *args, **options):
        """Punto de entrada del comando."""
        self.stdout.write('Esperando por la BD...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write(
                    'Base de datos no disponible, espere 1 segundo...'
                    )
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Base de datos disponible!'))
