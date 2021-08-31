from rest_framework.routers import SimpleRouter
from .views import DispositivoViewSet, DadosViewSet, ConfiguracaoViewSet, MensagensViewSet


router = SimpleRouter()
router.register('dispositivos', DispositivoViewSet)
router.register('dados', DadosViewSet)
router.register('configuracoes', ConfiguracaoViewSet)
router.register('mensagens', MensagensViewSet)
