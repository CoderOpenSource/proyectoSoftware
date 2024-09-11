from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tablero, Juego, Movimiento, HistorialPartida
from .serializers import TableroSerializer, JuegoSerializer, MovimientoSerializer, HistorialPartidaSerializer
from django.shortcuts import render
from django.contrib.auth.models import User

def test_websocket(request):
    return render(request, 'test_websocket.html')

class TableroViewSet(viewsets.ModelViewSet):
    queryset = Tablero.objects.all()
    serializer_class = TableroSerializer
    permission_classes = [IsAuthenticated]

class JuegoViewSet(viewsets.ModelViewSet):
    queryset = Juego.objects.all()
    serializer_class = JuegoSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def estado(self, request, pk=None):
        juego = self.get_object()
        tablero = juego.tablero
        return Response(tablero.estado)

    @action(detail=True, methods=['post'])
    def movimiento(self, request, pk=None):
        juego = self.get_object()
        jugador = request.user
        x = request.data.get('posicion_x')
        y = request.data.get('posicion_y')

        if juego.turno_actual != jugador:
            return Response({"detail": "No es tu turno."}, status=status.HTTP_400_BAD_REQUEST)

        if juego.tablero.estado[x][y] != "":
            return Response({"detail": "Movimiento inválido."}, status=status.HTTP_400_BAD_REQUEST)

        movimiento = Movimiento(juego=juego, jugador=jugador, posicion_x=x, posicion_y=y)
        movimiento.save()

        return Response({"detail": "Movimiento registrado."})

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [IsAuthenticated]

class HistorialPartidaViewSet(viewsets.ModelViewSet):
    queryset = HistorialPartida.objects.all()
    serializer_class = HistorialPartidaSerializer
    permission_classes = [IsAuthenticated]
