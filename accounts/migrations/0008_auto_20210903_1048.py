# Generated by Django 2.2.9 on 2021-09-03 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210903_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plano',
            name='limite_dispositivos_iot',
        ),
        migrations.RemoveField(
            model_name='plano',
            name='limite_redes_iot',
        ),
    ]
