from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TableroViewSet, JuegoViewSet, MovimientoViewSet, HistorialPartidaViewSet, test_websocket

router = DefaultRouter()
router.register(r'tableros', TableroViewSet)
router.register(r'juegos', JuegoViewSet)
router.register(r'movimientos', MovimientoViewSet)
router.register(r'historial', HistorialPartidaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test-websocket/', test_websocket, name='test_websocket'),
]
