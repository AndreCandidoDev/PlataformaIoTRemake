from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins

from .models import Dados, Dispositivo, Configuracoes, Mensagens
from .serializers import DadosSerializer, DispositivoSerializer, ConfiguracaoSerializer, MensagensSerializer


# POST only
class MensagensViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Mensagens.objects.all()
    serializer_class = MensagensSerializer


# POST only
class DadosViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Dados.objects.all()
    serializer_class = DadosSerializer


class ConfiguracaoViewSet(viewsets.GenericViewSet):
    queryset = Configuracoes.objects.all()
    serializer_class = ConfiguracaoSerializer


# GET only using id
class DispositivoViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Dispositivo.objects.all()
    serializer_class = DispositivoSerializer

    @action(detail=True, methods=['get'])
    def dados(self, request, pk=None):
        dispositivo = self.get_object()
        serializer = DadosSerializer(dispositivo.dados.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def configuracoes(self, request, pk=None):
        dispositivo = self.get_object()
        serializer = ConfiguracaoSerializer(dispositivo.configuracoes.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def mensagens(self, request, pk=None):
        dispositivo = self.get_object()
        serializer = MensagensSerializer(dispositivo.mensagens.all(), many=True)
        return Response(serializer.data)
