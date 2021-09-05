from rest_framework import serializers
from .models import Dispositivo, Dados, Configuracoes, Mensagens


class DadosSerializer(serializers.ModelSerializer):
    class Meta:

        model = Dados

        fields = (
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
            'limite_inferior',
            'limite_superior'
        )


class MensagensSerializer(serializers.ModelSerializer):
    class Meta:
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
    mensagens = MensagensSerializer(many=True, read_only=True)

    class Meta:
        extra_kwargs = {
            'id': {'write_only': True},
            'usuario': {'write_only': True},
        }

        model = Dispositivo

        fields = (
            'usuario',
            'nome',
            'serial',
            'placa',
            'tipo',
            'dados',
            'configuracoes',
            'mensagens',
            'criacao',
            'ativo'
        )

# =========================================== API V2 para usuarios pagos =========================================

