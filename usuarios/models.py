from django.db import models
from django.contrib.auth.models import User
import uuid

class Jugador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amigos = models.ManyToManyField('self', through='Amistad', symmetrical=False, related_name='mis_amigos')
    online = models.BooleanField(default=False)
    jugador_id = models.CharField(max_length=10, unique=True, default=uuid.uuid4().hex[:8].upper())
    fecha_registro = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.jugador_id:
            self.jugador_id = self.generate_unique_jugador_id()
        super().save(*args, **kwargs)

    def generate_unique_jugador_id(self):
        while True:
            jugador_id = uuid.uuid4().hex[:8].upper()
            if not Jugador.objects.filter(jugador_id=jugador_id).exists():
                return jugador_id

    def enviar_solicitud_amistad(self, jugador):
        SolicitudAmistad.objects.create(sender=self, receiver=jugador)

    def aceptar_solicitud_amistad(self, jugador):
        try:
            solicitud = SolicitudAmistad.objects.get(sender=jugador, receiver=self)
            Amistad.objects.create(from_jugador=self, to_jugador=jugador)
            Amistad.objects.create(from_jugador=jugador, to_jugador=self)
            solicitud.delete()
        except SolicitudAmistad.DoesNotExist:
            pass

    def rechazar_solicitud_amistad(self, jugador):
        try:
            solicitud = SolicitudAmistad.objects.get(sender=jugador, receiver=self)
            solicitud.delete()
        except SolicitudAmistad.DoesNotExist:
            pass

    def eliminar_amigo(self, jugador):
        Amistad.objects.filter(from_jugador=self, to_jugador=jugador).delete()
        Amistad.objects.filter(from_jugador=jugador, to_jugador=self).delete()

    def get_amigos(self):
        amigos_ids = Amistad.objects.filter(from_jugador=self).values_list('to_jugador', flat=True)
        return Jugador.objects.filter(id__in=amigos_ids)

    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()

class Amistad(models.Model):
    from_jugador = models.ForeignKey(Jugador, related_name='from_jugador', on_delete=models.CASCADE)
    to_jugador = models.ForeignKey(Jugador, related_name='to_jugador', on_delete=models.CASCADE)

class SolicitudAmistad(models.Model):
    sender = models.ForeignKey(Jugador, related_name='sent_solicitudes', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Jugador, related_name='received_solicitudes', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class EstadisticasJugador(models.Model):
    jugador = models.OneToOneField(Jugador, on_delete=models.CASCADE)
    ganados = models.IntegerField(default=0)
    perdidos = models.IntegerField(default=0)
    empatados = models.IntegerField(default=0)
    jugados = models.IntegerField(default=0)

    def __str__(self):
        return f"Estadísticas de {self.jugador.user.username}"
