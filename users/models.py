from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

cities = [
        ('BOG', 'Bogotá'),
        ('MED', 'Medellin'),
        ('CAL', 'Cali'),
    ]

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    tel = models.CharField(max_length=11)
    cel = models.CharField(max_length=11)
    doctype = models.CharField(max_length=2, choices=[
        ('CC', 'Cédula de Ciudadanía'), ('CE', 'Cédula de Extranjería')
        ])
    docnumber = models.PositiveIntegerField(null=True)
    city = models.CharField(max_length=3, choices=cities)
    last_update = models.DateTimeField(auto_now=True)
    verificated = models.BooleanField(default=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        indexes = [models.Index(fields=['email'])]
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
