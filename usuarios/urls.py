from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, JugadorViewSet, GroupViewSet, LoginView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'jugadores', JugadorViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),  # Agregar la ruta para la vista de inicio de sesión
]
