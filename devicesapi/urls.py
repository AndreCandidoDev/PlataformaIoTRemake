from rest_framework.routers import SimpleRouter
from .views import DispositivoViewSet, DadosViewSet


router = SimpleRouter()
router.register('dispositivos', DispositivoViewSet)
router.register('dados', DadosViewSet)