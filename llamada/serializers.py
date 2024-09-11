from rest_framework import serializers
from .models import Llamada

class LlamadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Llamada
        fields = '__all__'
        read_only_fields = ('estado', 'timestamp_inicio', 'timestamp_fin', 'canal')
