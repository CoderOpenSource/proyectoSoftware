import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AudioConnectorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Aceptar la conexión WebSocket
        await self.accept()
        print("WebSocket connection accepted")

    async def disconnect(self, close_code):
        # Desconexión de la WebSocket
        print(f"WebSocket disconnected with close code: {close_code}")

    async def receive(self, text_data):
        # Este método recibirá los datos del audio desde el WebSocket
        try:
            data = json.loads(text_data)
            audio_chunk = data.get('audio', None)

            if audio_chunk:
                # Aquí podrías procesar el audio o guardarlo en algún lugar
                print("Audio recibido:", audio_chunk)

            # Responder con algún mensaje de confirmación si es necesario
            await self.send(text_data=json.dumps({
                'status': 'Audio received',
            }))
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
            await self.send(text_data=json.dumps({
                'status': 'Error: Invalid JSON',
            }))
