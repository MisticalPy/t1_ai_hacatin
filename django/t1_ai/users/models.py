from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    phone = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Телефон",
        null=True,
        blank=True
    )
