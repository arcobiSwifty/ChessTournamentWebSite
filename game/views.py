from user.models import Player
#from .models import 

from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views import View
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView

from django.http import HttpResponseForbidden

class Home(View):
    def get(self, request):
        return render(request, 'home.html')