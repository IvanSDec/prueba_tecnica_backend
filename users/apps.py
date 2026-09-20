from django.apps import AppConfig

"""
    @AUTHOR: Ivan Sanchez
    @LAST_UPDATE: 2026-09-19
    @DESCRIPTION: Configuración de la aplicación de usuarios en el proyecto Django.
"""
#* Configuración de la aplicación de usuarios en el proyecto Django.
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
