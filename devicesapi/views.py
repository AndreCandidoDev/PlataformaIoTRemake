from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.views import APIView

from .models import Dados, Dispositivo, Configuracoes, Mensagens, Acoes
from accounts.models import Plano
from .serializers import DadosSerializer, DispositivoSerializer, \
    ConfiguracaoSerializer, MensagensSerializer, AcoesSerializer


# =========================  API Usuarios gratuitos ============================================================

class DispositivoApiView(APIView):
    def get(self, request, dispositivo_serial):
        dispositivo = Dispositivo.objects.filter(serial=dispositivo_serial)
        serializer = DispositivoSerializer(dispositivo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AcoesApiView(APIView):
    def get(self, request, dispositivo_serial):
        dispositivo = Dispositivo.objects.get(serial=dispositivo_serial)
        acao = Acoes.objects.filter(dispositivo=dispositivo)
        serializer = AcoesSerializer(acao, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DadosApiView(APIView):
    def post(self, request, dispositivo_serial):
        dispositivo = Dispositivo.objects.get(serial=dispositivo_serial)
        confs = Configuracoes.objects.get(dispositivo=dispositivo)
        try:
            plano = Plano.objects.get(usuario=request.user)
            if plano.plano == 'Pessoal':
                if dispositivo.dados.count() == 100:
                    return Response("Limite de dados atingido para esse dispositivo",
                                    status=status.HTTP_403_FORBIDDEN)
            elif plano.plano == 'Empresarial':
                if dispositivo.dados.count() == 1000:
                    return Response("Limite de dados atingido para esse dispositivo",
                                    status=status.HTTP_403_FORBIDDEN)
        except:
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
        try:
            plano = Plano.objects.get(usuario=request.user)
            if plano.plano == 'Pessoal':
                if dispositivo.mensagens.count() == 100:
                    return Response("Limite de mensagens atingido para esse dispositivo",
                                    status=status.HTTP_403_FORBIDDEN)
            elif plano.plano == 'Empresarial':
                if dispositivo.mensagens.count() == 1000:
                    return Response("Limite de mensagens atingido para esse dispositivo",
                                    status=status.HTTP_403_FORBIDDEN)
        except:
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
