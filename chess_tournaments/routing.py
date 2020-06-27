from channels.routing import ProtocolTypeRouter, URLRouter 
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack 
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from django.urls import path

from game.consumers import GameConsumer, NotificationConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    #path("partita/<int:pk>", PartitaConsumer),
                    path("gioco/<pk>", GameConsumer)
                ]
            )
        )
    )
})