from django.db import models
from accounts.models import Account


class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    # usuario = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Dispositivo(Base):
    tipo_dispositivo = (
        ('Atuador', 'atuador'),
        ('Sensor', 'sensor')
    )
    usuario = models.ForeignKey(Account, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    placa = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255, choices=tipo_dispositivo)

    class Meta:
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'
        ordering = ['id']

    def __str__(self):
        return self.nome


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
