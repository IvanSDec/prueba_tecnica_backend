from django.db import models

"""
    @AUTHOR: Ivan Sanchez
    @LAST_UPDATE: 2026-09-19
    @DESCRIPTION: Modelo para la gestión de Roles y Permisos mediante variables booleanas.
"""
#* Modelo Role para la gestión de roles y permisos mediante variables booleanas.
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    editar_usuarios = models.BooleanField(default=False)
    editar_personajes = models.BooleanField(default=False)
    ver_personajes = models.BooleanField(default=False)
    ver_usuarios = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"