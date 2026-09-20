from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('birth_date', 'phone_number', 'roles')}),
    )
    filter_horizontal = ('roles',)