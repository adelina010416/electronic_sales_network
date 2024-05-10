from rest_framework.routers import DefaultRouter

from traders.apps import TradersConfig
from traders.views import ItemViewSet, SalesNetworkViewSet, ProductViewSet

app_name = TradersConfig.name

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='items')
router.register(r'networks', SalesNetworkViewSet, basename='networks')
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [] + router.urls
