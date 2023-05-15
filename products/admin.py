from django.contrib import admin
from .models import *


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'state']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ['model', 'price', 'price_rrc']


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    list_display = ['value']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'city']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'state']


# список заказанных позиций
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_info', 'quantity']

