from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Jugador, SolicitudAmistad
from .serializers import UserSerializer, JugadorSerializer, GroupSerializer, LoginSerializer, SolicitudAmistadSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import AgregarAmigoSerializer, RechazarAmigoSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class JugadorViewSet(viewsets.ModelViewSet):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer

    @action(detail=True, methods=['get'])
    def amigos(self, request, pk=None):
        jugador = self.get_object()
        amigos = jugador.get_amigos()
        serializer = JugadorSerializer(amigos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def agregar_amigo(self, request, pk=None):
        jugador = self.get_object()
        serializer = AgregarAmigoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                amigo = Jugador.objects.get(pk=serializer.validated_data['amigo_id'])
                jugador.enviar_solicitud_amistad(amigo)
                return Response({'status': 'Solicitud de amistad enviada'}, status=status.HTTP_200_OK)
            except Jugador.DoesNotExist:
                return Response({'error': 'Jugador no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def aceptar_amigo(self, request, pk=None):
        jugador = self.get_object()
        serializer = AgregarAmigoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                amigo = Jugador.objects.get(pk=serializer.validated_data['amigo_id'])
                print(amigo)
                jugador.aceptar_solicitud_amistad(amigo)
                return Response({'status': 'Amistad aceptada'}, status=status.HTTP_200_OK)
            except Jugador.DoesNotExist:
                return Response({'error': 'Jugador no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def rechazar_amigo(self, request, pk=None):
        jugador = self.get_object()
        serializer = RechazarAmigoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                amigo = Jugador.objects.get(pk=serializer.validated_data['amigo_id'])
                jugador.rechazar_solicitud_amistad(amigo)
                return Response({'status': 'Solicitud de amistad rechazada'}, status=status.HTTP_200_OK)
            except Jugador.DoesNotExist:
                return Response({'error': 'Jugador no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def eliminar_amigo(self, request, pk=None):
        jugador = self.get_object()
        serializer = RechazarAmigoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                amigo = Jugador.objects.get(pk=serializer.validated_data['amigo_id'])
                jugador.eliminar_amigo(amigo)
                return Response({'status': 'Amigo eliminado'}, status=status.HTTP_200_OK)
            except Jugador.DoesNotExist:
                return Response({'error': 'Jugador no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def solicitudes_amigos_recibidas(self, request, pk=None):
        jugador = self.get_object()
        solicitudes = jugador.received_solicitudes.all()
        serializer = SolicitudAmistadSerializer(solicitudes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def solicitudes_amigos_enviadas(self, request, pk=None):
        jugador = self.get_object()
        solicitudes = jugador.sent_solicitudes.all()
        serializer = SolicitudAmistadSerializer(solicitudes, many=True)
        return Response(serializer.data)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        # Vamos a intentar autenticación con username ya que parece que tu modelo User usa username y no email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=user.username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Create token
        refresh = RefreshToken.for_user(user)

        # Get the photo URL if exists
        try:
            jugador = Jugador.objects.get(user=user)
            foto_url = jugador.avatar.url if jugador.avatar else None
        except Jugador.DoesNotExist:
            foto_url = None

        # Get groups
        groups = user.groups.values_list('name', flat=True)  # Obtiene los nombres de los grupos

        user_data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'email': user.email,
            'foto': foto_url,
            'groups': list(groups)  # Agrega los grupos del usuario
        }

        print(user_data['groups'])

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_data': user_data
        })
