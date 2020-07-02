from django.db import models
from user.models import Player

import string, random

import uuid

import chess

from decimal import Decimal

class Move(models.Model):

    text = models.CharField(max_length=8)
    index = models.IntegerField()
    duration = models.DecimalField(max_digits=7, decimal_places=2)
    color = models.IntegerField() #0 -> white, #1 -> black
    date = models.DateTimeField(auto_now_add=True)


class Game(models.Model):

    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    white_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="white")
    black_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="black")

    total_duration = models.IntegerField() #seconds
    increment = models.IntegerField() #seconds

    time_remaining_white = models.DecimalField(max_digits=7, decimal_places=2)
    time_remaining_black = models.DecimalField(max_digits=7, decimal_places=2)

    moves = models.ManyToManyField(Move)

    is_white_moving = models.BooleanField(default=True)

    start = models.DateTimeField(blank=True, null=True)
    started = models.BooleanField(default=False)
    start_timer = models.IntegerField(default=0)

    has_time = models.BooleanField(default=True)

    def get_game_object(self):
        moves = self.moves.order_by("index", "color")
        board = chess.Board()
        for move in moves:
            board.push_san(move.text)
        return board

    def add_move(self, text, index, duration, color):
        move = Move.objects.create(text=text, index=index, duration=duration, color=color)
        self.moves.add(move)
        if color == 0 and  self.has_time:
            self.time_remaining_white = self.time_remaining_white - Decimal.from_float(duration)
        elif color == 1 and self.has_time:
            self.time_remaining_black = self.time_remaining_black - Decimal.from_float(duration)
        self.save()

    def get_last_move(self):
        return self.moves.order_by("index", "color").last()

    def is_valid_move(self, move_count):
        if move_count == self.moves.count():
            print(move_count, self.moves.count())
            return False 
        return True
        



    
    