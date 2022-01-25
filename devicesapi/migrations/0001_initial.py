# Generated by Django 3.2.11 on 2022-01-19 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('networks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispositivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
                ('nome', models.CharField(max_length=255)),
                ('serial', models.SlugField(max_length=255, unique=True)),
                ('placa', models.CharField(max_length=255)),
                ('tipo', models.CharField(choices=[('Atuador', 'atuador'), ('Sensor', 'sensor')], max_length=255)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Dispositivo',
                'verbose_name_plural': 'Dispositivos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Mensagens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
                ('alerta', models.CharField(max_length=255)),
                ('mensagem', models.CharField(max_length=255)),
                ('is_critic', models.BooleanField(default=False)),
                ('dispositivo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mensagens', to='devicesapi.dispositivo')),
                ('dispositivo_rede', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mensagens_dispositivo_rede', to='networks.dispositivorede')),
            ],
            options={
                'verbose_name': 'Mensagens',
                'verbose_name_plural': 'Mensagens',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Dados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
                ('unidade', models.CharField(max_length=255)),
                ('dado', models.CharField(max_length=255)),
                ('dispositivo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dados', to='devicesapi.dispositivo')),
                ('dispositivo_rede', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dados_dispositivo_rede', to='networks.dispositivorede')),
            ],
            options={
                'verbose_name': 'Dados',
                'verbose_name_plural': 'Dados',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Configuracoes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
                ('limite_inferior', models.CharField(default='0', max_length=255)),
                ('limite_superior', models.CharField(default='100', max_length=255)),
                ('dispositivo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='configuracoes', to='devicesapi.dispositivo')),
                ('dispositivo_rede', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='configuracoes_dispositivo_rede', to='networks.dispositivorede')),
            ],
            options={
                'verbose_name': 'Configuracao',
                'verbose_name_plural': 'Configuracoes',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Acoes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
                ('pino', models.IntegerField(default=4)),
                ('sinal', models.CharField(choices=[('Ligado', 'True'), ('Desligado', 'False')], default='True', max_length=255)),
                ('dispositivo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='acoes', to='devicesapi.dispositivo')),
                ('dispositivo_rede', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='acoes_dispositivo_rede', to='networks.dispositivorede')),
            ],
            options={
                'verbose_name': 'Acao',
                'verbose_name_plural': 'Acoes',
                'ordering': ['id'],
            },
        ),
    ]
