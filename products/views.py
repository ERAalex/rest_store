from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .email_confirmation import confirmation_order_email, confirmation_order_email_for_shop

import yaml
from rest_framework.viewsets import ModelViewSet
from yaml import load as load_yaml, Loader

from requests import get
from core.filters import ShopFilter
from .serializers import ProductListSerializer, ProductSerializer, OrderItemSerializer, OrderSerializer, ShopSerializer
from .models import *
from users_part.models import ContactUser
from users_part.serializers import ContactUserSerializer


class PartnerUpdate(APIView):
    """
    Класс для обновления прайса от поставщика
    """

    def post(self, request):
        if request.user.is_partner is False:
            return Response({'status': 'You are not partner!'})

        '''Сохранение файла из POST запроса'''
        result = request.FILES['file']
        destination = open('media/' + result.name, 'wb+')
        for chunk in result.chunks():
            destination.write(chunk)
        destination.close()

        '''Открываем файл и обновляем данные - можно сделать через celery'''
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

                ProductInfo.objects.filter(shop_id=shop.id).delete()
                for good in goods:
                    product, _ = Product.objects.get_or_create(id=good['id'], name=good['name'],
                                                               category_id=good['category'])

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
    queryset = Shop.objects.all()
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
        id_data = self.kwargs['id']
        return Product.objects.filter(id=id_data)


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

        '''Ищем только корзины со статусом - confirmed - со стороны пользователя и только для конкретного продавца'''

        order = Order.objects.filter(
            ordered_items__product_info__shop__user_account_id=request.user.id, state='confirmed')

        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)


class BasketView(APIView):

    def post(self, request):
        ''' Загрузка списка OrderItems в корзину - принимает список'''

        user_id = request.user

        if type(request.data) is not list:
            return Response({'error': 'Не корректный ввод, должен быть список'})

        dict_information = dict()
        for data_item in request.data:
            quantity_items = data_item['quantity']
            product_id = int(data_item['product_info'])

            try:
                quantity_items = int(quantity_items)
            except ValueError:
                return Response({'error': 'Количество товара указано не цифрой'})

            if quantity_items <= 0:
                return Response({'error': 'Вы ввели не корректное количество товара'})

            ''' проверяем есть ли такой товар по ID и сразу проверяем количесто в магазинах '''
            try:
                product_info = ProductInfo.objects.filter(id=product_id)
                product_check = product_info[0].product
                total_quantity_shops = sum([item.quantity for item in product_info])
                if total_quantity_shops == 0:
                    return Response({'error': f'Товара {product_info.model} нет в наличии'})

                if quantity_items > total_quantity_shops:
                    quantity_items = total_quantity_shops

            except Exception as e:
                print(e)
                return Response({'error': f'Вы ввели не правильный ID продукта - {product_id}, перепроверьте данные'})

            ''' Создаем корзину, потом создаем итемы корзины и добавляем их в нее'''
            try:
                order, create_order_items = Order.objects.get_or_create(user=user_id, state='basket')
                OrderItem.objects.get_or_create(
                    order=order,
                    # нам нужен тут 0, тк это список из разных магазинов нашего товара, берем 1 (одинаковые товары)
                    product_info=product_info[0],
                    quantity=quantity_items
                )

            except Exception as e:
                print(e)
                return Response({'error': 'Не удалось сохранить товар в корзину'})

            dict_information['order'] = order
            dict_information[f'{product_check.name}'] = f'количество товара  : {quantity_items}'

        return Response({'Статус': f'Товары занесены в корзину: {dict_information["order"]}. '
                                   f'Товар: {dict_information}.'})

    def get(self, request):
        '''Получить все корзины пользователя'''

        user_id = request.user
        try:
            order = Order.objects.get(user=user_id, state='basket')
        except:
            return Response({'Error': f'Корзина отсутвует, добавьте сначало предметы'})

        product = OrderItem.objects.filter(order=order)

        dict_result = dict()
        for items in product:
            dict_result[f'{items.id} - {items.product_info.product}'] = f'количество товара - {items.quantity}'

        return Response({f'Всего в корзине № {order.id} товаров': f'{dict_result}'})

    def put(self, request):
        ''' Обновление корзины - принимает список'''

        user_id = request.user

        if type(request.data) is not list:
            return Response({'error': 'Не корректный ввод, должен быть список'})

        dict_information = dict()

        for data_item in request.data:
            quantity_items = data_item['quantity']
            product_id = int(data_item['id'])

            try:
                quantity_items = int(quantity_items)
            except ValueError:
                return Response({'error': 'Количество товара указано не цифрой'})

            if quantity_items <= 0:
                return Response({'error': 'Вы ввели не корректное количество товара'})

            ''' проверяем есть ли такой товар по ID и сразу првоеряем количесто в магазинах '''
            try:
                order_item_get = OrderItem.objects.get(id=product_id)
                total_quantity_in_shops = order_item_get.product_info.quantity

                if total_quantity_in_shops == 0:
                    return Response({'error': f'Товара {order_item_get.model} нет в наличии'})

                if quantity_items > total_quantity_in_shops:
                    quantity_items = total_quantity_in_shops

            except Exception as e:
                print(e)
                return Response({'error': f'Вы ввели не правильный ID продукта - {product_id}, перепроверьте данные'})

            try:
                order = Order.objects.get(user=user_id, state='basket')
                order_item = OrderItem.objects.filter(id=product_id).update(
                    quantity=quantity_items
                )

            except ValueError as e:
                print(e)
                return Response({'error': 'Не удалось сохранить товар в корзину'})

            dict_information['order'] = order
            dict_information[f'{order_item_get.product_info.product.name}'] = f'количество товара  : {quantity_items}'

        return Response({'Статус': f'Товары изменены в корзине: {dict_information["order"]}. '
                                   f'Товар: {dict_information}.'})


class OrderConfirmationByUserView(APIView):
    """
    Подтверждение заказа пользователем
    """
    def patch(self, request):
        user_id = request.user.id

        ''' проверяем есть ли контактная информация перед подтверждением корзины '''
        check_contact_adress = ContactUser.objects.filter(user=user_id)

        if not check_contact_adress:
            return Response({'Error': 'Отсутсвует адрес доставки'})

        order_id = request.data['order_id']
        if not order_id:
            return Response({'Error': 'Не указан номер заказа'})

        try:
            ''' поиск заказа по id '''
            order = Order.objects.get(id=order_id, state='basket')
            order_items = OrderItem.objects.filter(order=order_id)
        except:
            return Response({'Error': 'Заказ для подтверждения не существует'})


        product_infos = {}


        ''' проходимся по каждому продукту в заказе, чтобы проверить наличие в магазине и подредактировать + цена '''
        for item in order_items:
            ''' проверка существующего количества в магазине'''
            total_quantity_available = int(item.product_info.quantity)
            ''' количества товара в заказе '''
            quantity = item.quantity
            ''' проверка, есть ли товар в наличии '''
            if total_quantity_available == 0:
                return Response({'Error': 'Товар раскуплен'})
            ''' если товара в наличии меньше, чем в заказе '''
            order_quantity = total_quantity_available if quantity > total_quantity_available else quantity
            ''' если настоящее количество товара в заказе отличается от рассчитаного, то выбери рассчитаную '''
            if quantity != order_quantity:
                item.quantity = order_quantity
                item.save()
            ''' рассчет цены '''
            price = float(item.product_info.price) * order_quantity
            ''' информация по товарам записывается в словарь '''
            product_infos[item.id] = (item.product_info.product.name, item.product_info.model, order_quantity, price,)

        try:
            ''' готовим адрес покупателя для сообщений email '''
            address_person = ContactUser.objects.filter(user=user_id)
            address_dict = ContactUserSerializer(address_person[0]).data
            ''' если все товары в наличии - изменяем количество в самом магазине + готовим словарь из магазинов'''
            shops = dict()

            for item in order_items:
                product_info_save = ProductInfo.objects.get(id=item.product_info.id)
                product_info_save.quantity = product_info_save.quantity - item.quantity
                product_info_save.save()
                try:
                    shops[item.product_info.shop.user_account.email] += [[item.id, item.product_info.product.name,
                                                                         item.quantity]]
                except:
                    shops[item.product_info.shop.user_account.email] = [[item.id, item.product_info.product.name,
                                                                        item.quantity]]

            ''' рассылаем конкретно каждому магазину из заказа номер заказа и детали по конкретно его товарам'''
            confirmation_order_email_for_shop(shops, order_id, address_dict)

            ''' подтверждение заказа с необходимыми параметрами '''
            address_person = ContactUser.objects.filter(user=user_id)
            address_dict = ContactUserSerializer(address_person[0]).data
            confirmation_order_email(request.user.email, request.user.name, order_id, product_infos, address_dict)

            ''' изменение статуса заказа '''
            Order.objects.filter(id=order_id).update(state='confirmed', user=user_id)

            return Response({'Ok': f'заказ {order.id} успешно подтвержден'})

        except ValueError as e:
            print(e)
            return Response({'Error': 'Ошибка во время подтверждения заказа'})




