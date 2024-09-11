import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from chat.middleware import TokenAuthMiddlewareStack
from chat.routing import juego_websocket_urlpatterns
from juego.routing import websocket_urlpatterns
from llamada.routing import llamadas_websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tictactoe.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns + juego_websocket_urlpatterns + llamadas_websocket_urlpatterns
        )
    ),
})
