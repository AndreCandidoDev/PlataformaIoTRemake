from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins

from .models import Dados, Dispositivo, Configuracoes
from .serializers import DadosSerializer, DispositivoSerializer, ConfiguracaoSerializer


class DadosViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Dados.objects.all()
    serializer_class = DadosSerializer


class ConfiguracaoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Configuracoes.objects.all()
    serializer_class = ConfiguracaoSerializer


class DispositivoViewSet(viewsets.ModelViewSet):
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
