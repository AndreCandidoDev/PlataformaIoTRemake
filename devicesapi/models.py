from django.db import models
from accounts.models import Account
from networks.models import DispositivoRede


class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True


# todo: criar o tipo de dispositivo misto que possuirá ação e configuração
# dispositivo de usuário gratuito
class Dispositivo(Base):
    tipo_dispositivo = (
        ('Atuador', 'atuador'),
        ('Sensor', 'sensor')
    )
    usuario = models.ForeignKey(Account, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    serial = models.SlugField(max_length=255, unique=True)
    placa = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255, choices=tipo_dispositivo)

    class Meta:
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'
        ordering = ['id']

    def __str__(self):
        return self.nome


# =====================================================================================================================
# plano gratuito: apenas uma ação/configuração por instancia de dispositivo
# planos pagos: multiplas ações/configurações a depender da placa do dispositivo
# todo: instanciar multiplas ações/configurações a depender da tecnologia do dispositivo

# somente atuadores
class Acoes(Base):
    sinais = (
        ('Ligado', 'True'),
        ('Desligado', 'False')
    )
    dispositivo = models.ForeignKey(Dispositivo, related_name='acoes', on_delete=models.CASCADE,
                                    null=True, blank=True)
    dispositivo_rede = models.ForeignKey(DispositivoRede, related_name='acoes_dispositivo_rede', on_delete=models.CASCADE,
                                         null=True, blank=True)
    pino = models.IntegerField(default=4)
    sinal = models.CharField(max_length=255, choices=sinais, default='True')

    class Meta:
        verbose_name = 'Acao'
        verbose_name_plural = 'Acoes'
        ordering = ['id']

    def __str__(self):
        return str(self.id)


# somente sensores
class Configuracoes(Base):
    dispositivo = models.ForeignKey(Dispositivo, related_name='configuracoes', on_delete=models.CASCADE,
                                    null=True, blank=True)
    dispositivo_rede = models.ForeignKey(DispositivoRede, related_name='configuracoes_dispositivo_rede', on_delete=models.CASCADE,
                                         null=True, blank=True)
    limite_inferior = models.CharField(max_length=255, default='0')
    limite_superior = models.CharField(max_length=255, default='100')

    class Meta:
        verbose_name = 'Configuracao'
        verbose_name_plural = 'Configuracoes'
        ordering = ['id']

    def __str__(self):
        return str(self.id)
# =====================================================================================================================


class Dados(Base):
    dispositivo = models.ForeignKey(Dispositivo, related_name='dados', on_delete=models.CASCADE,
                                    null=True, blank=True)
    dispositivo_rede = models.ForeignKey(DispositivoRede, related_name='dados_dispositivo_rede', on_delete=models.CASCADE,
                                         null=True, blank=True)
    unidade = models.CharField(max_length=255)
    dado = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Dados'
        verbose_name_plural = 'Dados'
        ordering = ['id']

    def __str__(self):
        return f'Dados de {self.dispositivo}'


class Mensagens(Base):
    dispositivo = models.ForeignKey(Dispositivo, related_name='mensagens', on_delete=models.CASCADE,
                                    null=True, blank=True)
    dispositivo_rede = models.ForeignKey(DispositivoRede, related_name='mensagens_dispositivo_rede', on_delete=models.CASCADE,
                                         null=True, blank=True)
    alerta = models.CharField(max_length=255)
    mensagem = models.CharField(max_length=255)
    is_critic = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Mensagens'
        verbose_name_plural = 'Mensagens'
        ordering = ['id']

    def __str__(self):
        return f'{self.alerta} em {self.dispositivo}'
