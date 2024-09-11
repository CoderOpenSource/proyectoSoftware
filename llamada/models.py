from django.db import models
from django.utils import timezone
from usuarios.models import Jugador
import uuid

class Llamada(models.Model):
    AUDIO = 'audio'
    VIDEO = 'video'
    TIPOS_LLAMADA = [
        (AUDIO, 'Audio'),
        (VIDEO, 'Video')
    ]

    INICIADA = 'iniciada'
    EN_CURSO = 'en_curso'
    TERMINADA = 'terminada'
    ESTADOS_LLAMADA = [
        (INICIADA, 'Iniciada'),
        (EN_CURSO, 'En curso'),
        (TERMINADA, 'Terminada')
    ]

    iniciador = models.ForeignKey(Jugador, related_name='llamadas_iniciadas', on_delete=models.CASCADE)
    receptor = models.ForeignKey(Jugador, related_name='llamadas_recibidas', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=5, choices=TIPOS_LLAMADA, default=AUDIO)
    estado = models.CharField(max_length=10, choices=ESTADOS_LLAMADA, default=INICIADA)
    timestamp_inicio = models.DateTimeField(auto_now_add=True)
    timestamp_fin = models.DateTimeField(null=True, blank=True)
    canal = models.CharField(max_length=100, default=uuid.uuid4().hex)

    def __str__(self):
        return f"Llamada de {self.iniciador} a {self.receptor} ({self.tipo})"

    def iniciar(self):
        self.estado = self.EN_CURSO
        self.timestamp_inicio = timezone.now()
        self.save()

    def finalizar(self):
        self.estado = self.TERMINADA
        self.timestamp_fin = timezone.now()
        self.save()
