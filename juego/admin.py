from django.contrib import admin
from .models import Juego, Tablero, Movimiento, HistorialPartida

admin.site.register(Juego)
admin.site.register(Tablero)
admin.site.register(Movimiento)
admin.site.register(HistorialPartida)
