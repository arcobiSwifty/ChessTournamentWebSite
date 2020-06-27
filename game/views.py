from user.models import Player
from .models import Game, Move

from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views import View
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView

from django.http import HttpResponseForbidden

import random

class Home(View):
    def get(self, request):
        return render(request, 'home.html')

class CreateGame(View):
    def get(self, request, pk):
        opponent = Player.objects.get(id=pk)
        #change
        if bool(random.getrandbits(1)):
            game = Game.objects.create(white_player=request.user, black_player=opponent, total_duration=600, increment=2, time_remaining_white=600, time_remaining_black=600)
        else:
            game = Game.objects.create(white_player=opponent, black_player=request.user, total_duration=600, increment=2, time_remaining_white=600, time_remaining_black=600)
        return redirect("/gioco/%s" % game.code) 

class GameView(View):
    def get(self, request, pk):
        return render(request, "game.html")