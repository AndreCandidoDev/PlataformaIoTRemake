from django.db import models
from accounts.models import Account


class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True


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


class Configuracoes(Base):
    dispositivo = models.ForeignKey(Dispositivo, related_name='configuracoes', on_delete=models.CASCADE)
    limite_inferior = models.CharField(max_length=255, default='0')
    limite_superior = models.CharField(max_length=255, default='100')

    def __str__(self):
        return str(self.dispositivo)


class Dados(Base):
    dispositivo = models.ForeignKey(Dispositivo, related_name='dados', on_delete=models.CASCADE)
    unidade = models.CharField(max_length=255)
    dado = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Dados'
        verbose_name_plural = 'Dados'
        ordering = ['id']

    def __str__(self):
        return f'Dados de {self.dispositivo}'


class Mensagens(Base):
    dispositivo = models.ForeignKey(Dispositivo, related_name='mensagens', on_delete=models.CASCADE)
    alerta = models.CharField(max_length=255)
    mensagem = models.CharField(max_length=255)
    is_critic = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Mensagens'
        verbose_name_plural = 'Mensagens'
        ordering = ['id']

    def __str__(self):
        return f'{self.alerta} em {self.dispositivo}'
