from django.db import models
from users.models import CustomUser


class Lawyer(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    profesional_card = models.CharField(max_length=20)
    webpage = models.URLField(blank=True)
    linked_in = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    active = models.BooleanField(default=False)
    last_check = models.DateTimeField(null=True, default=None)

    def __str__(self):
        pass

    class Meta:
        verbose_name = 'Lawyer'
        verbose_name_plural = 'Lawyers'
