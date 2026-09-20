from rest_framework.permissions import BasePermission

"""
AUTHOR: Ivan Sanchez
LAST_UPDATE: 2026-09-19
DESCRIPTION: Permisos personalizados basados en las banderas de rol del usuario.
"""

class CanViewUsers(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.roles.filter(ver_usuarios=True).exists()


class CanEditUsers(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.roles.filter(editar_usuarios=True).exists()