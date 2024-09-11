from django.urls import path
from .views import generar_sesion_vonage

# Define las rutas manualmente
urlpatterns = [
    path('generar_sesion_vonage/', generar_sesion_vonage, name='generar_sesion_vonage'),
]
    
