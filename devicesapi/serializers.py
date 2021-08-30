from rest_framework import serializers
from .models import Dispositivo, Dados, Configuracoes


class DadosSerializer(serializers.ModelSerializer):
    class Meta:

        model = Dados

        fields = (
            'id',
            'dispositivo',
            'unidade',
            'dado',
            'criacao',
            # 'ativo'
        )


class ConfiguracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracoes

        fields = (
            'id',
            'dispositivo',
            'limite_inferior',
            'limite_superior'
        )


class DispositivoSerializer(serializers.ModelSerializer):

    dados = DadosSerializer(many=True, read_only=True)
    configuracoes = ConfiguracaoSerializer(many=True, read_only=True)

    class Meta:
        extra_kwargs = {
            'usuario': {'write_only': True}
        }

        model = Dispositivo

        fields = (
            'id',
            'usuario',
            'nome',
            'placa',
            'tipo',
            'dados',
            'configuracoes',
            'criacao',
            'ativo'
        )
