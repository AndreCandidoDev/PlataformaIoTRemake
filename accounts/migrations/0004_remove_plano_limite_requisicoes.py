# Generated by Django 2.2.9 on 2021-09-03 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_plano'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plano',
            name='limite_requisicoes',
        ),
    ]
