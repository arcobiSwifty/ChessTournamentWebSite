from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views import View
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth import login, authenticate

from .models import Player
from .forms import SignupForm

class SignupView(FormView):
    form_class = SignupForm
    template_name = "registration/register.html"
    def form_valid(self, form):
        form.save()
        cleaned_data = form.cleaned_data 
        user = authenticate(username=cleaned_data.get("username"), password=form.cleaned_data.get("password1"))
        login(self.request, user)
        return redirect("/")
        #todo: implement email confirmation

class PlayerDetail(DetailView):
    template_name = "profile.html"
    model = Player 

class ProfileDetail(DetailView):
    template_name = "profile.html"
    model = Player

    def get_object(self, queryset=None):
        return self.request.user
