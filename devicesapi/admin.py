from django.contrib import admin
from .models import Dispositivo, Dados, Configuracoes

# Register your models here.

admin.site.register(Dispositivo)
admin.site.register(Dados)
admin.site.register(Configuracoes)