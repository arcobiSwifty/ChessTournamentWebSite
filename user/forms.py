from django import forms
from .models import Player 
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = Player 
        fields = ('username', 'email', 'password1', 'password2')