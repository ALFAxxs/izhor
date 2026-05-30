from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN    = 'admin',    'Admin'
        MERCHANT = 'merchant', 'Merchant'

    role        = models.CharField(max_length=20, choices=Role.choices, default=Role.MERCHANT)
    phone       = models.CharField(max_length=20, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
