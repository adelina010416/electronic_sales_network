from django.db import models
from rest_framework.exceptions import ValidationError

from constants import nullable


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name='название')
    model = models.CharField(max_length=250, verbose_name='модель')
    release_date = models.DateField(
        verbose_name='дата выхода продукта на рынок')

    def __str__(self):
        return f"{self.name} {self.model}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class NetworkItem(models.Model):
    TYPE_CHOICES = (
        ('factory', 'завод'),
        ('retail network', 'розничная сеть'),
        ('individual entrepreneur', 'ИП')
    )
    name = models.CharField(max_length=100, verbose_name='название')
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, verbose_name='тип')
    email = models.EmailField(verbose_name='почта')
    country = models.CharField(verbose_name='страна')
    city = models.CharField(verbose_name='город')
    street = models.CharField(verbose_name='улица')
    house = models.CharField(verbose_name='номер дома')
    products = models.ManyToManyField(
        Product, **nullable, verbose_name='продукты')
    supplier = models.ForeignKey(
        "self", on_delete=models.CASCADE, **nullable, verbose_name='поставщик')
    debt = models.DecimalField(
        max_digits=10, default=0.00,
        decimal_places=2, verbose_name='задолженность')
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name='время и дата создания')

    def __str__(self):
        return f"{self.type} {self.name}"

    class Meta:
        verbose_name = 'Звено сети'
        verbose_name_plural = 'Звенья сети'


class SalesNetwork(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    manufacturer = models.ForeignKey(
        NetworkItem, on_delete=models.CASCADE,
        related_name='manufacturer',
        verbose_name='производитель')
    distributor = models.ForeignKey(
        NetworkItem,
        **nullable, on_delete=models.CASCADE,
        related_name='distributor',
        verbose_name='распространитель')
    consumer = models.ForeignKey(
        NetworkItem, on_delete=models.CASCADE,
        related_name='consumer',
        verbose_name='потребитель')

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        if self.distributor:
            if self.distributor.supplier != self.manufacturer:
                raise ValidationError(
                    "Указанный распространитель не является потребителем "
                    "указанного производителя!")
            if self.consumer.supplier != self.distributor:
                raise ValidationError(
                    "Указанный потребитель не является потребителем "
                    "указанного распространителя!")
        else:
            if self.consumer.supplier != self.manufacturer:
                raise ValidationError(
                    "Указанный потребитель не является потребителем "
                    "указанного производителя!")

    class Meta:
        verbose_name = 'Торговая сеть'
        verbose_name_plural = 'Торговые сети'
