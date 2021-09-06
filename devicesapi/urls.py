from django.urls import path
from .views import DispositivoApiView, DadosApiView, MensagensApiView

# from rest_framework.routers import SimpleRouter
# from .views import DispositivoViewSet, DadosViewSet, ConfiguracaoViewSet, MensagensViewSet

urlpatterns = [
    path('dispositivos/<slug:dispositivo_serial>/', DispositivoApiView.as_view(), name='dispositivos'),
    path('dados/<slug:dispositivo_serial>/', DadosApiView.as_view(), name='dados'),
    path('mensagens/<slug:dispositivo_serial>/', MensagensApiView.as_view(), name='mensagens')
]

# router = SimpleRouter()
# router.register('dispositivos', DispositivoViewSet)
# router.register('dados', DadosViewSet)
# router.register('configuracoes', ConfiguracaoViewSet)
# router.register('mensagens', MensagensViewSet)
