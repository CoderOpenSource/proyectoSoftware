from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, MensajeViewSet, test_websocket
router = DefaultRouter()
router.register(r'chats', ChatViewSet)
router.register(r'mensajes', MensajeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('prueba_chat/', test_websocket, name='test_websocket')
]
