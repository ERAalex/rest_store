from django.core.validators import URLValidator
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError
import yaml
from yaml import load as load_yaml, Loader

from requests import get

from .models import *


class PartnerUpdate(APIView):
    """
    Класс для обновления прайса от поставщика
    """

    def post(self, request):
        with open("media/shop1.yaml") as stream:
            try:
                data = load_yaml(stream, Loader=Loader)
                shop_data = data['shop']
                categories = data['categories']
                goods = data['goods']
                shop, _ = Shop.objects.get_or_create(name=shop_data)
                for category_data in categories:
                    category, _ = Category.objects.get_or_create(id=category_data['id'], name=category_data['name'])
                    category.shops.add(shop.id)
                    category.save()
                for good in goods:
                    product, _ = Product.objects.get_or_create(id=good['id'], name=good['name'], category_id=good['category'])

                    product_info = ProductInfo.objects.create(
                        product=product,
                        shop=shop,
                        model=good['model'],
                        price=good['price'],
                        price_rrc=good['price_rrc'],
                        quantity=good['quantity'])
                    for name, value in good['parameters'].items():
                        parameter_object, _ = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.create(
                            product_info=product_info,
                            parameter=parameter_object,
                            value=value)
            except yaml.YAMLError as exc:
                return Response({'status':'Error', 'message': exc})
        return Response({'status':'OK'})