from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Jugador, EstadisticasJugador, Amistad, SolicitudAmistad

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'groups']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'email': {'required': False},
            'username': {'required': False}  # Asegurarse de que el username no sea obligatorio en la actualización
        }

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user.groups.set(groups)
        return user

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)
        password = validated_data.pop('password', None)

        # Remover username de los datos validados si está presente
        if 'username' in validated_data:
            validated_data.pop('username')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        if groups is not None:
            instance.groups.set(groups)
        return instance

class EstadisticasJugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadisticasJugador
        fields = ['ganados', 'perdidos', 'empatados', 'jugados']

class JugadorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    estadisticas = serializers.SerializerMethodField()

    class Meta:
        model = Jugador
        fields = ['id', 'user', 'online', 'jugador_id', 'fecha_registro', 'avatar', 'estadisticas', 'last_seen']

    def get_estadisticas(self, obj):
        try:
            estadisticas = EstadisticasJugador.objects.get(jugador=obj)
            return EstadisticasJugadorSerializer(estadisticas).data
        except EstadisticasJugador.DoesNotExist:
            return None

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        jugador = Jugador.objects.create(user=user, **validated_data)
        EstadisticasJugador.objects.create(jugador=jugador)
        return jugador

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        if user_data:
            # Remover username de los datos del usuario si está presente
            if 'username' in user_data:
                user_data.pop('username')
            UserSerializer().update(instance.user, user_data)

        instance.online = validated_data.get('online', instance.online)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()

        return instance

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

class AgregarAmigoSerializer(serializers.Serializer):
    amigo_id = serializers.IntegerField()

class RechazarAmigoSerializer(serializers.Serializer):
    amigo_id = serializers.IntegerField()

class SolicitudAmistadSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField(source='sender.id')
    receiver_id = serializers.IntegerField(source='receiver.id')
    sender_username = serializers.CharField(source='sender.user.username')
    receiver_username = serializers.CharField(source='receiver.user.username')
    sender_avatar = serializers.CharField(source='sender.avatar')
    receiver_avatar = serializers.CharField(source='receiver.avatar')

    class Meta:
        model = SolicitudAmistad
        fields = ['id', 'sender_id', 'receiver_id', 'sender_username', 'receiver_username', 'sender_avatar', 'receiver_avatar', 'timestamp']
