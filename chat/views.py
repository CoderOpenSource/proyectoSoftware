from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from usuarios.models import Jugador
from .models import Chat, Mensaje
from .serializers import ChatSerializer, MensajeSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chat = serializer.save()
        # Agregar el jugador actual como participante del chat
        jugador = self.request.user.jugador
        chat.participantes.add(jugador)
        # Agregar otros participantes especificados en la solicitud
        participantes_ids = self.request.data.get('participantes', [])
        if participantes_ids:
            participantes = Jugador.objects.filter(id__in=participantes_ids)
            chat.participantes.add(*participantes)

class MensajeViewSet(viewsets.ModelViewSet):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        jugador = self.request.user.jugador
        serializer.save(remitente=jugador)

    @action(detail=False, methods=['get'])
    def chat(self, request):
        chat_id = request.query_params.get('chat')
        if chat_id:
            mensajes = self.queryset.filter(chat_id=chat_id)
            serializer = self.get_serializer(mensajes, many=True)
            return Response(serializer.data)
        return Response({"error": "chat parameter is required"}, status=400)

def test_websocket(request):
    return render(request, 'test_chat_websocket.html')
