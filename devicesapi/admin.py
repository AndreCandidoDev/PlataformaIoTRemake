from django.contrib import admin
from .models import Dispositivo, Dados, Configuracoes, Mensagens

# Register your models here.

admin.site.register(Dispositivo)
admin.site.register(Dados)
admin.site.register(Configuracoes)
admin.site.register(Mensagens)
