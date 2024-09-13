from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, CustomerViewSet, CardViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'cards', CardViewSet)

urlpatterns = router.urls
