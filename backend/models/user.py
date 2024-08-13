# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, blank=True)

    # Cambiar el related_name para evitar conflictos
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Cambia este nombre según sea necesario
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Cambia este nombre según sea necesario
        blank=True,
    )

    def __str__(self):
        return self.username