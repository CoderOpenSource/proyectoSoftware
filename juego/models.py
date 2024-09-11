from django.db import models
from django.contrib.auth.models import User

class Tablero(models.Model):
    estado = models.JSONField(default=dict)  # Representación del tablero como JSON

    def __str__(self):
        return f"Tablero del Juego {self.id}"

    def verificar_estado(self):
        estado = self.estado
        for i in range(3):
            if estado[i][0] == estado[i][1] == estado[i][2] != "":
                return estado[i][0]
            if estado[0][i] == estado[1][i] == estado[2][i] != "":
                return estado[0][i]
        if estado[0][0] == estado[1][1] == estado[2][2] != "":
            return estado[0][0]
        if estado[0][2] == estado[1][1] == estado[2][0] != "":
            return estado[0][2]
        if all(all(cell != "" for cell in row) for row in estado):
            return "Empate"
        return None

class Juego(models.Model):
    ESTADO_CHOICES = [
        ('EN PROGRESO', 'En progreso'),
        ('FINALIZADO', 'Finalizado'),
    ]

    jugador1 = models.ForeignKey(User, related_name='juegos_como_jugador1', on_delete=models.CASCADE)
    jugador2 = models.ForeignKey(User, related_name='juegos_como_jugador2', on_delete=models.CASCADE)
    ganador = models.ForeignKey(User, related_name='juegos_ganados', on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='EN PROGRESO')
    turno_actual = models.ForeignKey(User, related_name='juegos_en_turno', on_delete=models.CASCADE)
    tablero = models.OneToOneField(Tablero, on_delete=models.CASCADE, related_name='juego')

    def __str__(self):
        return f"Juego {self.id} entre {self.jugador1.username} y {self.jugador2.username}"

    def verificar_estado(self):
        resultado = self.tablero.verificar_estado()
        if resultado:
            self.estado = "FINALIZADO"
            if resultado == "Empate":
                self.ganador = None
            else:
                self.ganador = User.objects.get(username=resultado)
            self.save()

class Movimiento(models.Model):
    juego = models.ForeignKey(Juego, related_name='movimientos', on_delete=models.CASCADE)
    jugador = models.ForeignKey(User, on_delete=models.CASCADE)
    posicion_x = models.IntegerField()
    posicion_y = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    tiempo_restante = models.IntegerField(default=30)  # Tiempo en segundos para realizar la acción

    def __str__(self):
        return f"Movimiento de {self.jugador.username} en Juego {self.juego.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        tablero = self.juego.tablero
        estado = tablero.estado
        estado[self.posicion_x][self.posicion_y] = self.jugador.username
        tablero.estado = estado
        tablero.save()
        self.juego.verificar_estado()

class HistorialPartida(models.Model):
    jugador = models.ForeignKey(User, related_name='historial_partidas', on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, related_name='historial', on_delete=models.CASCADE)
    resultado = models.CharField(max_length=10)  # Ganado, Perdido, Empate
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.jugador.username} - {self.resultado} en Juego {self.juego.id}"
