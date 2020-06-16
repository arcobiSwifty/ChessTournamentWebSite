from django.db import models
from django.contrib.auth.models import AbstractUser

class Player(AbstractUser):
    following = models.ManyToManyField("Player")
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


