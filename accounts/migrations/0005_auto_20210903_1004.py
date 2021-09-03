# Generated by Django 2.2.9 on 2021-09-03 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_plano_limite_requisicoes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plano',
            name='unidade_tempo',
        ),
        migrations.AlterField(
            model_name='plano',
            name='periodo',
            field=models.IntegerField(choices=[('Trimestral', '3 meses'), ('Semestral', '6 meses'), ('anual', '1 ano')], default='Trimestral'),
        ),
    ]
