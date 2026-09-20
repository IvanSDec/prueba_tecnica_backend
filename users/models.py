from django.contrib.auth.models import AbstractUser
from django.db import models
from roles.models import Role  # Importamos el modelo Role

class User(AbstractUser):
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relación M2M: Un Usuario puede tener uno o más Roles
    roles = models.ManyToManyField(
        Role,
        related_name='users',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    # Método helper para verificar rápidamente permisos desde el código
    def has_permission(self, permission_code):
        if self.is_superuser:
            return True
        return self.roles.filter(permissions__code=permission_code).exists()