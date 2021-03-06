# Generated by Django 3.2.11 on 2022-01-19 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
                ('nome_rede', models.CharField(max_length=255, null=True)),
                ('limite_dispositivos_rede', models.IntegerField(default=10)),
                ('qtd_dispositivos_rede', models.IntegerField(default=0)),
                ('identificador', models.CharField(max_length=255)),
                ('plano', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.plano')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MetricasRede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
                ('taxa_de_dados', models.FloatField(blank=True, default=0.0, null=True)),
                ('taxa_de_mensagens', models.FloatField(blank=True, default=0.0, null=True)),
                ('dados_consumidos', models.FloatField(blank=True, default=0.0, null=True)),
                ('rede', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='networks.rede')),
            ],
            options={
                'verbose_name': 'Metricas-Rede',
                'verbose_name_plural': 'Metricas-Rede',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DispositivoRede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
                ('ip', models.CharField(max_length=14)),
                ('nome', models.CharField(max_length=255)),
                ('serial', models.SlugField(max_length=255, unique=True)),
                ('placa', models.CharField(max_length=255)),
                ('tipo', models.CharField(choices=[('Atuador', 'atuador'), ('Sensor', 'sensor')], max_length=255)),
                ('rede', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='networks.rede')),
            ],
            options={
                'verbose_name': 'Dispositivo-Rede',
                'verbose_name_plural': 'Dispositivos-Rede',
                'ordering': ['id'],
            },
        ),
    ]
