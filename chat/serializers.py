from rest_framework import serializers
from django.contrib.auth.models import User

from usuarios.models import Jugador
from .models import Chat, Mensaje

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class JugadorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Jugador
        fields = ['id', 'username']
class MensajeSerializer(serializers.ModelSerializer):
    remitente = JugadorSerializer(read_only=True)

    class Meta:
        model = Mensaje
        fields = ['id', 'chat', 'remitente', 'contenido', 'timestamp']

class ChatSerializer(serializers.ModelSerializer):
    participantes = JugadorSerializer(many=True, read_only=True)
    mensajes = MensajeSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'participantes', 'mensajes']
