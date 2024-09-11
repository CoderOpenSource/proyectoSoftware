from django.db import models
from usuarios.models import Jugador

class Chat(models.Model):
    participantes = models.ManyToManyField(Jugador, related_name='chats')

    def __str__(self):
        return f"Chat {self.id}"

class Mensaje(models.Model):
    chat = models.ForeignKey(Chat, related_name='mensajes', on_delete=models.CASCADE)
    remitente = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    contenido = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
