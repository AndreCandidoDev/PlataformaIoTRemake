from django.db import models
from accounts.models import Plano, UserProfile, Account


class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Rede(Base):
    usuario = models.ForeignKey(Account, on_delete=models.CASCADE)
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE)
    nome_rede = models.CharField(max_length=255, null=True)
    limite_dispositivos_rede = models.IntegerField(default=10)
    qtd_dispositivos_rede = models.IntegerField(default=0)
    identificador = models.CharField(max_length=255)

    def __str__(self):
        return str(self.nome_rede)


class DispositivoRede(Base):
    tipo_dispositivo = (
        ('Atuador', 'atuador'),
        ('Sensor', 'sensor')
    )
    rede = models.ForeignKey(Rede, on_delete=models.CASCADE)
    ip = models.CharField(max_length=14)
    nome = models.CharField(max_length=255)
    serial = models.SlugField(max_length=255, unique=True)
    placa = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255, choices=tipo_dispositivo)

    class Meta:
        verbose_name = 'Dispositivo-Rede'
        verbose_name_plural = 'Dispositivos-Rede'
        ordering = ['id']

    def __str__(self):
        return self.nome


class MetricasRede(Base):
    rede = models.ForeignKey(Rede, on_delete=models.CASCADE)
    taxa_de_dados = models.FloatField(blank=True, null=True, default=0.0)
    taxa_de_mensagens = models.FloatField(blank=True, null=True, default=0.0)
    dados_consumidos = models.FloatField(blank=True, null=True, default=0.0)

    class Meta:
        verbose_name = 'Metricas-Rede'
        verbose_name_plural = 'Metricas-Rede'
        ordering = ['id']

    def __str__(self):
        return f'Metricas da rede {str(self.rede)}'
