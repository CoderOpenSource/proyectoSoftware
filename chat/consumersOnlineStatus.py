# chat/consumersOnlineStatus.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'online_status'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Obtener el token y el ID del jugador de la query string
        query_params = dict(item.split('=') for item in self.scope['query_string'].decode().split('&'))
        token = query_params.get('token')
        jugador_id = query_params.get('jugadorId')

        await self.accept()

        # Establecer el estado en línea del usuario
        await self.set_user_online_status(jugador_id, True)

    async def disconnect(self, close_code):
        # Obtener el ID del jugador de la query string
        query_params = dict(item.split('=') for item in self.scope['query_string'].decode().split('&'))
        jugador_id = query_params.get('jugadorId')

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Establecer el estado en línea del usuario a False y actualizar la última vez en línea
        await self.set_user_online_status(jugador_id, False)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_status_message',
                'message': message
            }
        )

    async def online_status_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def set_user_online_status(self, jugador_id, status):
        from usuarios.models import Jugador  # Mover la importación aquí para evitar ciclos

        @database_sync_to_async
        def set_status():
            try:
                jugador = Jugador.objects.get(id=jugador_id)
                jugador.online = status
                if not status:
                    jugador.last_seen = timezone.now()
                jugador.save()
                return {
                    'user_id': jugador.user.id,
                    'online': status,
                    'last_seen': jugador.last_seen.isoformat() if jugador.last_seen else None
                }
            except Jugador.DoesNotExist:
                return None

        status_info = await set_status()
        if status_info:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'online_status_update',
                    'userId': status_info['user_id'],
                    'online': status_info['online'],
                    'last_seen': status_info['last_seen']
                }
            )

    async def online_status_update(self, event):
        await self.send(text_data=json.dumps({
            'userId': event['userId'],
            'online': event['online'],
            'last_seen': event['last_seen']
        }))
