from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from traders.models import NetworkItem, SalesNetwork, Product
from traders.serializers import NetworkItemSerializer, \
    SalesNetworkSerializer, ProductSerializer


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = NetworkItemSerializer
    queryset = NetworkItem.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('country', 'type',)


class SalesNetworkViewSet(viewsets.ModelViewSet):
    serializer_class = SalesNetworkSerializer
    queryset = SalesNetwork.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('manufacturer', 'distributor', 'consumer',)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
