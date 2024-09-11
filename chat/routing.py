from django.urls import path

from .consumersChat import ChatConsumer
from .consumersOnlineStatus import OnlineStatusConsumer

juego_websocket_urlpatterns = [
    path('ws/online_status/', OnlineStatusConsumer.as_asgi()),
    path('ws/chat/', ChatConsumer.as_asgi()),]
