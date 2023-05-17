from django.core.validators import URLValidator
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError
import yaml
from rest_framework.viewsets import ModelViewSet
from yaml import load as load_yaml, Loader

from requests import get
from core.filters import ShopFilter
from .serializers import ProductListSerializer, ProductSerializer, OrderItemSerializer, OrderSerializer, ShopSerializer
from .models import *


class PartnerUpdate(APIView):
    """
    Класс для обновления прайса от поставщика
    """

    def post(self, request):
        if request.user.is_partner is False:
            return Response({'status': 'You are not partner!'})

        # сохраняем файл из post запроса
        result = request.FILES['file']
        destination = open('media/' + result.name, 'wb+')
        for chunk in result.chunks():
            destination.write(chunk)
        destination.close()

        # открываем и обновляем БД
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
                return Response({'status': 'Error', 'message': exc})
        return Response({'status': 'OK'})


class ShopViewSet(ModelViewSet):
    """
    Просмотреть все доступные магазины
    """
    queryset =Shop.objects.all()
    serializer_class = ShopSerializer
    http_method_names = ['get', ]
    permission_classes = [AllowAny]



class ProductsViewSet(ModelViewSet):
    """
    Просмотреть все товары, фильтрация по категоориям и магазинам
    """
    queryset = Category.objects.all()
    serializer_class = ProductListSerializer
    http_method_names = ['get', ]
    filterset_class = ShopFilter


class ProductsItemViewSet(ModelViewSet):
    """
    Просмотреть конкретный товар по его id
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', ]
    filterset_class = ShopFilter

    def get_queryset(self):
        id = self.kwargs['id']
        return Product.objects.filter(id=id)


class OrderItemViewSet(ModelViewSet):
    """
    Показать все продукты добавленные в корзину
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    http_method_names = ['get', 'put', 'delete']
    filterset_class = ShopFilter

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PartnerOrdersView(APIView):
    """
    Отображение всех заказов для магазинов - владельцев
    """
    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Only for registered users'}, status=403)

        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Only shops'}, status=403)

        order = Order.objects.filter(
            ordered_items__product_info__shop__user_account_id=request.user.id).exclude(state='basket').prefetch_related(
            'ordered_items__product_info__product__category')

        serializer = OrderSerializer(order, many=True)

        return Response(serializer.data)



class BasketView(APIView):

    def post(self, request):
        user_id = request.user

        if type(request.data) is not list:
            return Response({'error': 'Не корректный ввод, должен быть список'})

        dicc_information = dict()
        for data_item in request.data:
            quantity_items = data_item['quantity']
            product_id = int(data_item['product_info'])

            try:
                quantity_items = int(quantity_items)
            except ValueError:
                return Response({'error': 'Количество товара указано не цифрой'})

            if quantity_items <= 0:
                return Response({'error': 'Вы ввели не корректное количество товара'})

            ''' проверяем есть ли такой товар по ID и сразу првоеряем количесто в магазинах '''
            try:
                product_info = ProductInfo.objects.filter(id=product_id)
                product_check = product_info[0].product
                total_quantity_shops = sum([item.quantity for item in product_info])
                if total_quantity_shops == 0:
                    return Response({'error': 'Товара нет в наличии'})

                if quantity_items > total_quantity_shops:
                    quantity_items = total_quantity_shops

            except Exception as e:
                print(e)
                return Response({'error': 'Вы ввели не правильный ID продукта, перепроверьте данные'})

            ''' Создаем корзину, потом создаем итемы корзины и добавляем их в нее'''
            try:
                order, create_order_items = Order.objects.get_or_create(user=user_id, state='basket')
                OrderItem.objects.get_or_create(
                    order=order,
                    # нам нужен тут 0, тк это список из разных магазинов нашего товара, берем 1, тк это один и тотже товарs
                    product_info=product_info[0],
                    quantity=quantity_items
                )
            except Exception as e:
                print(e)
                return Response({'error': 'Не удалось сохранить товар в корзину'})

            dicc_information['order'] = order
            dicc_information[f'{product_check.name}'] = f'количество товара  : {quantity_items}'


        return Response({'Статус': f'Товары занесены в корзину: {dicc_information["order"]}. '
                                   f'Товар: {dicc_information}.'})









