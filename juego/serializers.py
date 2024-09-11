from rest_framework import serializers
from .models import Tablero, Juego, Movimiento, HistorialPartida
from django.contrib.auth.models import User

class TableroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tablero
        fields = ['id', 'estado']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class JuegoSerializer(serializers.ModelSerializer):
    jugador1 = UserSerializer(read_only=True)
    jugador2 = UserSerializer(read_only=True)
    ganador = UserSerializer(read_only=True, allow_null=True)
    turno_actual = UserSerializer(read_only=True)
    tablero = TableroSerializer()

    class Meta:
        model = Juego
        fields = ['id', 'jugador1', 'jugador2', 'ganador', 'fecha', 'estado', 'turno_actual', 'tablero']

    def create(self, validated_data):
        tablero_data = validated_data.pop('tablero')
        tablero = Tablero.objects.create(**tablero_data)
        juego = Juego.objects.create(tablero=tablero, **validated_data)
        return juego

class MovimientoSerializer(serializers.ModelSerializer):
    jugador = UserSerializer(read_only=True)

    class Meta:
        model = Movimiento
        fields = ['id', 'juego', 'jugador', 'posicion_x', 'posicion_y', 'timestamp', 'tiempo_restante']

    def create(self, validated_data):
        jugador = self.context['request'].user
        movimiento = Movimiento.objects.create(jugador=jugador, **validated_data)
        return movimiento

class HistorialPartidaSerializer(serializers.ModelSerializer):
    jugador = UserSerializer(read_only=True)
    juego = JuegoSerializer(read_only=True)

    class Meta:
        model = HistorialPartida
        fields = ['id', 'jugador', 'juego', 'resultado', 'fecha']
