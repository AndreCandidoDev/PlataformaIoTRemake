from django.contrib import admin
from .models import Dispositivo, Dados, Configuracoes, Mensagens, Acoes

# Register your models here.

admin.site.register(Dispositivo)
admin.site.register(Dados)
admin.site.register(Configuracoes)
admin.site.register(Acoes)
admin.site.register(Mensagens)
