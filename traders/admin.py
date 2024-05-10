from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from traders.models import NetworkItem, SalesNetwork, Product


@admin.action(description="Очистить задолженность")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0.00)


@admin.register(NetworkItem)
class NetworkItemAdmin(admin.ModelAdmin):
    """Регистрация модели NetworkItem в админке"""
    list_display = ('id', 'name', 'type',
                    'link_to_supplier',
                    'debt', 'creation_date',)
    list_filter = ('type', 'city',)
    search_fields = ('name',)
    actions = [clear_debt]

    def link_to_supplier(self, obj):
        if obj.supplier:
            link = reverse("admin:traders_networkitem_change",
                           args=[obj.supplier.id])
            return format_html(
                u'<a href="%s">%s</a>' % (link, obj.supplier.name))
    link_to_supplier.allow_tags = True


@admin.register(SalesNetwork)
class SalesNetworkAdmin(admin.ModelAdmin):
    """Регистрация модели SalesNetwork в админке"""
    list_display = ('id', 'name',
                    'link_to_manufacturer',
                    'link_to_distributor',
                    'link_to_consumer',)

    def link_to_manufacturer(self, obj):
        link = reverse("admin:traders_networkitem_change",
                       args=[obj.manufacturer.id])
        return format_html(
            u'<a href="%s">%s</a>' % (link, obj.manufacturer.name))

    def link_to_distributor(self, obj):
        if obj.distributor:
            link = reverse(
                "admin:traders_networkitem_change", args=[obj.distributor.id])
            return format_html(
                u'<a href="%s">%s</a>' % (link, obj.distributor.name))

    def link_to_consumer(self, obj):
        link = reverse(
            "admin:traders_networkitem_change", args=[obj.consumer.id])
        return format_html(u'<a href="%s">%s</a>' % (link, obj.consumer.name))

    link_to_manufacturer.allow_tags = True
    link_to_distributor.allow_tags = True
    link_to_consumer.allow_tags = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Регистрация модели Product в админке"""
    list_display = ('id', 'name', 'model',)
