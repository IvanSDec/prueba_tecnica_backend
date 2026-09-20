import pymysql
from django.conf import settings
from django.core.management.base import BaseCommand

"""
  @AUTHOR: Ivan Sanchez
  @LAST_UPDATE: 2026-09-19
  @DESCRIPTION: Comando personalizado para crear la base de datos MySQL si no existe.
  @NOTE: Ejecutar antes de 'python manage.py migrate'.
"""
class Command(BaseCommand):
    help = 'Crea la base de datos MySQL configurada en settings.py si no existe.'

    def handle(self, *args, **options):
      
        #* Obtenemos la configuración de la base de datos 'default' desde settings
        db_config = settings.DATABASES['default']
        db_name = db_config['NAME']
        db_user = db_config['USER']
        db_password = db_config['PASSWORD']
        db_host = db_config.get('HOST', 'localhost')
        db_port = int(db_config.get('PORT', 3306) or 3306)

        self.stdout.write(f"Verificando la base de datos '{db_name}' en {db_host}:{db_port}...")

        try:
            #* Conectamos al servidor MySQL sin especificar la base de datos
            connection = pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                port=db_port
            )

            with connection.cursor() as cursor:
              
                #* Verificar si la base de datos ya existe
                cursor.execute(f"SHOW DATABASES LIKE '{db_name}';")
                db_exists = cursor.fetchone()

                if db_exists:
                    self.stdout.write(self.style.WARNING(f"La base de datos '{db_name}' ya existe."))
                else:
                    #* Crear la base de datos si no existe
                    sql = f"CREATE DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
                    cursor.execute(sql)
                    self.stdout.write(self.style.SUCCESS(f"¡Base de datos '{db_name}' creada correctamente!"))

            connection.close()

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error al intentar verificar/crear la base de datos: {e}"))
        finally:
            #* Aseguramos que la conexión se cierre correctamente al finalizar.
            if 'connection' in locals() and connection.open:
                connection.close()