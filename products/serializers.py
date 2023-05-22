from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *
from users_part.models import ContactUser


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ['name']


class ParameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parameter
        fields = ['name']


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = ParameterSerializer(many=False)

    class Meta:
        model = ProductParameter
        fields = ['parameter', 'value', ]


class ProductInfoSerializer(serializers.ModelSerializer):
    shop = ShopSerializer(many=False)
    product_parameters = ProductParameterSerializer(many=True)

    class Meta:
        model = ProductInfo
        fields = ['price', 'price_rrc', 'shop', 'quantity', 'product_parameters', ]
        extra_kwargs = {
            'price_rrc': {'write_only': True},
        }


class ProductSerializer(serializers.ModelSerializer):
    product_info = ProductInfoSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'product_info']


class ProductListSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['category', 'products']
        extra_kwargs = {
            'category': {'source': 'name', 'read_only': True}
        }


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUser
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()

    class Meta:
        model = Order
        fields = ['dt', 'id', 'contact', 'state']


class OrderItemSerializer(serializers.ModelSerializer):
    product_info = ProductInfoSerializer
    order = OrderSerializer

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product_info', 'quantity']


