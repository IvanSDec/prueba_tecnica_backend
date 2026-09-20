from django.contrib import admin
from .models import Role

"""
    @AUTHOR: Ivan Sanchez
    @LAST_UPDATE: 2026-09-19
    @DESCRIPTION: Configuración del panel de administración para el modelo Role con flags de permisos.
"""
#* Registro del modelo Role en el panel de administración de Django.
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'name', 
        'editar_usuarios', 
        'editar_personajes', 
        'ver_personajes', 
        'ver_usuarios'
    )
    list_filter = ('editar_usuarios', 'editar_personajes', 'ver_personajes', 'ver_usuarios')
    search_fields = ('name',)