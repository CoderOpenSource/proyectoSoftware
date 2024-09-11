from django.urls import path
from .consumers import AudioConnectorConsumer

llamadas_websocket_urlpatterns = [
    path('ws/audio/', AudioConnectorConsumer.as_asgi()),
]
