import os
import sys
import threading
from django.apps import AppConfig
from utils.colors import Color, print_colored

""" 
AUTHOR: Ivan Sanchez
LAST_UPDATE: 2026-09-19
DESCRIPTION: Configuración de la aplicación Character y sincronización inicial de personajes.
"""
def run_sync():
    try:
        from .services import fetch_and_save_characters
        print_colored("Iniciando sincronización de los primeros 200 personajes...", Color.CYAN)
        result = fetch_and_save_characters(target_count=200)
        print_colored(
            f"Sincronización finalizada. Procesados: {result['processed_characters']} | Nuevos agregados: {result['new_characters_added']}", 
            Color.GREEN
        )
    except Exception as e:
        print_colored(f"Error al sincronizar personajes: {e}", Color.YELLOW)

class CharacterConfig(AppConfig):
    #* Configuración de la aplicación Character.
    default_auto_field = 'django.db.models.BigAutoField'
    #* Nombre de la aplicación.
    name = 'character'

    def ready(self):
        #* Método que se ejecuta cuando la aplicación está lista.
        is_server = any(arg in sys.argv for arg in ['runserver', 'gunicorn', 'uvicorn'])
        #* Verificar si el servidor está en ejecución y si es el proceso principal.
        if is_server and os.environ.get('RUN_MAIN') == 'true':
            #* Ejecutar la sincronización inicial en un hilo separado para no bloquear el inicio de Django.
            threading.Thread(target=run_sync, daemon=True).start()