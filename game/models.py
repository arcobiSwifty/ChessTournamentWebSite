from django.db import models
from user.models import Player

import string, random

import uuid

class Move(models.Model):

    text = models.CharField(max_length=8)
    index = models.IntegerField()
    duration = models.DecimalField(max_digits=7, decimal_places=3)
    color = models.IntegerField() #0 -> white, #1 -> black


class Game(models.Model):

    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    white_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="white")
    black_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="black")

    total_duration = models.IntegerField() #seconds
    increment = models.IntegerField() #seconds

    time_remaining_white = models.DecimalField(max_digits=7, decimal_places=3)
    time_remaining_black = models.DecimalField(max_digits=7, decimal_places=3)

    moves = models.ManyToManyField(Move)

    is_white_moving = models.BooleanField(default=True)

    start = models.DateTimeField(blank=True, null=True)
    