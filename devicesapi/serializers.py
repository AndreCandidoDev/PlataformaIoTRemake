from rest_framework import serializers
from .models import Dispositivo, Dados, Configuracoes, Mensagens, Acoes


class DadosSerializer(serializers.ModelSerializer):
    class Meta:

        model = Dados

        extra_kwargs = {
            'dispositivo': {'write_only': True}
        }

        fields = (
            'dispositivo',
            'unidade',
            'dado',
            'criacao',
        )


class ConfiguracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracoes

        fields = (
            'limite_inferior',
            'limite_superior'
        )


class AcoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acoes
        fields = (
            'pino',
            'sinal'
        )


class MensagensSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'dispositivo': {'write_only': True}
        }

        model = Mensagens

        fields = (
            'dispositivo',
            'alerta',
            'mensagem',
            'is_critic'
        )


# Todo: criar regra para identificador serial (não devemos usar id pois o mesmo é sequencial)
class DispositivoSerializer(serializers.ModelSerializer):

    dados = DadosSerializer(many=True, read_only=True)
    configuracoes = ConfiguracaoSerializer(many=True, read_only=True)
    acoes = AcoesSerializer(many=True, read_only=True)
    mensagens = MensagensSerializer(many=True, read_only=True)

    class Meta:
        extra_kwargs = {
            'id': {'write_only': True},
            'usuario': {'write_only': True},
            'serial': {'write_only': True},
        }

        model = Dispositivo

        fields = (
            'usuario',
            'nome',
            'placa',
            'tipo',
            'dados',
            'configuracoes',
            'acoes',
            'mensagens',
            'criacao',
            'ativo'
        )

