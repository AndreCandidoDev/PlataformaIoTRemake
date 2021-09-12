from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.views import APIView

from .models import Dados, Dispositivo, Configuracoes, Mensagens
from .serializers import DadosSerializer, DispositivoSerializer, ConfiguracaoSerializer, MensagensSerializer


# =========================  API Usuarios gratuitos ============================================================

class DispositivoApiView(APIView):
    def get(self, request, dispositivo_serial):
        dispositivo = Dispositivo.objects.filter(serial=dispositivo_serial)
        serializer = DispositivoSerializer(dispositivo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DadosApiView(APIView):
    def post(self, request, dispositivo_serial):
        dispositivo = Dispositivo.objects.get(serial=dispositivo_serial)
        confs = Configuracoes.objects.get(dispositivo=dispositivo)
        if dispositivo.dados.count() == 20:
            return Response("Limite de dados atingido para esse dispositivo",
                            status=status.HTTP_403_FORBIDDEN)
        request.data['dispositivo'] = str(dispositivo.id)
        if float(request.data['dado']) < float(confs.limite_inferior) \
                or float(request.data['dado']) > float(confs.limite_superior):
            return Response("Valor está fora da faixa de configuração", status=status.HTTP_400_BAD_REQUEST)
        serializer = DadosSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MensagensApiView(APIView):
    def post(self, request, dispositivo_serial):
        dispositivo = Dispositivo.objects.get(serial=dispositivo_serial)
        if dispositivo.mensagens.count() == 20:
            return Response("Limite de mensagens atingido para esse dispositivo",
                            status=status.HTTP_403_FORBIDDEN)
        request.data['dispositivo'] = str(dispositivo.id)
        serializer = MensagensSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#  ===========================================BACKUP===========================================================
# POST only
# class MensagensViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     queryset = Mensagens.objects.all()
#     serializer_class = MensagensSerializer
#
#
# # POST only
# class DadosViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     queryset = Dados.objects.all()
#     serializer_class = DadosSerializer
#
#
# class ConfiguracaoViewSet(viewsets.GenericViewSet):
#     queryset = Configuracoes.objects.all()
#     serializer_class = ConfiguracaoSerializer
#
#
# # GET only using id
# class DispositivoViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     queryset = Dispositivo.objects.all()
#     serializer_class = DispositivoSerializer
#
#     @action(detail=True, methods=['get'])
#     def dados(self, request, pk=None):
#         dispositivo = self.get_object()
#         serializer = DadosSerializer(dispositivo.dados.all(), many=True)
#         return Response(serializer.data)
#
#     @action(detail=True, methods=['get'])
#     def configuracoes(self, request, pk=None):
#         dispositivo = self.get_object()
#         serializer = ConfiguracaoSerializer(dispositivo.configuracoes.all(), many=True)
#         return Response(serializer.data)
#
#     @action(detail=True, methods=['get'])
#     def mensagens(self, request, pk=None):
#         dispositivo = self.get_object()
#         serializer = MensagensSerializer(dispositivo.mensagens.all(), many=True)
#         return Response(serializer.data)
