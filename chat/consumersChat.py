import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string'].decode()
        params = dict(param.split('=') for param in query_string.split('&'))
        self.token = params.get('token')  # Obtener el token de la consulta
        self.user_id = params.get('jugadorId')  # Obtener el jugadorId de la consulta

        if not self.user_id or not self.token:
            await self.close()
            return

        self.user_group_name = f'chat_user_{self.user_id}'

        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"Connected to user group: {self.user_group_name} with token: {self.token}")

    async def disconnect(self, close_code):
        print(f"Disconnecting from user group: {self.user_group_name} with close code {close_code}")
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(f"Message received: {text_data}")
        data = json.loads(text_data)

        if 'action' in data and data['action'] == 'subscribe':
            chat_id = data['chat_id']
            room_group_name = f'chat_{chat_id}'

            await self.channel_layer.group_add(
                room_group_name,
                self.channel_name
            )
            print(f"Subscribed to chat: {room_group_name}")

        elif 'action' in data and data['action'] == 'unsubscribe':
            chat_id = data['chat_id']
            room_group_name = f'chat_{chat_id}'

            await self.channel_layer.group_discard(
                room_group_name,
                self.channel_name
            )
            print(f"Unsubscribed from chat: {room_group_name}")

        elif 'contenido' in data and 'chat' in data and 'remitente' in data:
            contenido = data['contenido']
            chat_id = data['chat']
            remitente_id = data['remitente']

            chat = await self.get_chat(chat_id)
            remitente = await self.get_remitente(remitente_id)
            mensaje = await self.create_mensaje(chat, remitente, contenido)
            print(f"Message created: {mensaje}")

            room_group_name = f'chat_{chat_id}'

            await self.channel_layer.group_send(
                room_group_name,
                {
                    'type': 'chat_message',
                    'contenido': mensaje.contenido,
                    'remitente_id': remitente.id,
                    'username': await self.get_username(remitente),
                    'timestamp': str(mensaje.timestamp),
                    'chat_id': chat_id,
                }
            )
            print(f"Message sent to room group: {room_group_name}")

    async def chat_message(self, event):
        print(f"Message to send to WebSocket: {event}")
        contenido = event['contenido']
        remitente_id = event['remitente_id']
        username = event['username']
        timestamp = event['timestamp']
        chat_id = event['chat_id']

        await self.send(text_data=json.dumps({
            'contenido': contenido,
            'remitente_id': remitente_id,
            'username': username,
            'timestamp': timestamp,
            'chat_id': chat_id,
        }))

    @database_sync_to_async
    def get_chat(self, chat_id):
        from .models import Chat
        return Chat.objects.get(id=chat_id)

    @database_sync_to_async
    def get_remitente(self, remitente_id):
        from usuarios.models import Jugador
        return Jugador.objects.get(id=remitente_id)

    @database_sync_to_async
    def create_mensaje(self, chat, remitente, contenido):
        from .models import Mensaje
        return Mensaje.objects.create(chat=chat, remitente=remitente, contenido=contenido)

    @database_sync_to_async
    def get_username(self, remitente):
        return remitente.user.username
