import os
import sys
from django.apps import AppConfig
from utils.colors import Color, print_colored

""" 
AUTHOR: Ivan Sanchez
LAST_UPDATE: 2026-09-19
DESCRIPTION: Configuración e inicialización de roles predeterminados en la base de datos.
"""
def setup_default_roles():
    from .models import Role

    #* Configuración de roles predeterminados
    ROLES_CONFIG = {
        'Administrador': {
            'editar_usuarios': True,
            'editar_personajes': True,
            'ver_personajes': True,
            'ver_usuarios': True,
        },
        'Editor': {
            'editar_usuarios': False,
            'editar_personajes': True,
            'ver_personajes': True,
            'ver_usuarios': True,
        },
        'Lector': {
            'editar_usuarios': False,
            'editar_personajes': False,
            'ver_personajes': True,
            'ver_usuarios': False,
        },
    }

    print_colored("Verificando y sincronizando roles en la base de datos...", Color.CYAN)
    
    #* Iteramos sobre la configuración de roles y sincronizamos con la base de datos
    for role_name, permissions in ROLES_CONFIG.items():
        role, created = Role.objects.get_or_create(name=role_name)
        for perm, value in permissions.items():
            setattr(role, perm, value)
        role.save()

        if created:
            print_colored(f"Rol '{role_name}' creado exitosamente.", Color.GREEN)
        else:
            print_colored(f"Permisos del rol '{role_name}' actualizados correctamente.", Color.GREEN)
    print_colored("Configuración de roles finalizada.\n", Color.CYAN)

#* Configuración de la aplicación de roles y ejecución de la inicialización de roles predeterminados
class RolesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'roles'

    def ready(self):
        is_server = any(arg in sys.argv for arg in ['runserver', 'gunicorn', 'uvicorn'])
        if is_server and os.environ.get('RUN_MAIN') == 'true':
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                setup_default_roles()