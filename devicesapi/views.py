from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins

from .models import Dados, Dispositivo
from .serializers import DadosSerializer, DispositivoSerializer


class DadosViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Dados.objects.all()
    serializer_class = DadosSerializer


class DispositivoViewSet(viewsets.ModelViewSet):
    queryset = Dispositivo.objects.all()
    serializer_class = DispositivoSerializer

    @action(detail=True, methods=['get'])
    def dados(self, request, pk=None):
        dispositivo = self.get_object()
        serializer = DadosSerializer(dispositivo.dados.all(), many=True)
        return Response(serializer.data)