from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


"""
    @AUTHOR: Ivan Sanchez
    @LAST_UPDATE: 2026-09-19
    @DESCRIPTION: Configuración del panel de administración para el modelo User.
"""
#* Registro del modelo User en el panel de administración de Django.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('birth_date', 'phone_number', 'roles')}),
    )
    filter_horizontal = ('roles',)