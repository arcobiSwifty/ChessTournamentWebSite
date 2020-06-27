from django.urls import path

from .views import *

urlpatterns = [
    path("", Home.as_view()),
    path("sfida/<int:pk>", CreateGame.as_view()),
    path("gioco/<pk>", GameView.as_view()),
]
