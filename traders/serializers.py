from rest_framework import serializers

from traders.models import NetworkItem, Product, SalesNetwork


class NetworkItemSerializer(serializers.ModelSerializer):
    products = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )
    supplier = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = NetworkItem
        fields = '__all__'
        extra_kwargs = {
            'debt': {'read_only': True},
            'creation_date': {'read_only': True}
        }


class ProductSerializer(serializers.ModelSerializer):
    providers = NetworkItemSerializer(
        source='networkitem_set', read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'


class SalesNetworkSerializer(serializers.ModelSerializer):
    manufacturer = serializers.SlugRelatedField(
        many=False,
        queryset=NetworkItem.objects.all(),
        slug_field='name'
    )
    distributor = serializers.SlugRelatedField(
        many=False,
        queryset=NetworkItem.objects.all(),
        slug_field='name',
        required=False
    )
    consumer = serializers.SlugRelatedField(
        many=False,
        queryset=NetworkItem.objects.all(),
        slug_field='name'
    )

    def validate(self, data):
        manufacturer = data.get('manufacturer')
        distributor = data.get('distributor')
        consumer = data.get('consumer')
        if distributor:
            if distributor.supplier != manufacturer:
                raise serializers.ValidationError(
                    "Указанный распространитель не является потребителем "
                    "указанного производителя!")
            if consumer:
                if consumer.supplier != distributor:
                    raise serializers.ValidationError(
                        "Указанный потребитель не является потребителем "
                        "указанного распространителя!")
        else:
            if consumer:
                if consumer.supplier != manufacturer:
                    raise serializers.ValidationError(
                        "Указанный потребитель не является потребителем "
                        "указанного производителя!")
        return data

    class Meta:
        model = SalesNetwork
        fields = '__all__'
