from celery import shared_task
from django.core.mail import EmailMultiAlternatives, send_mail
from core import settings
from yaml import load as load_yaml, Loader
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter
from rest_framework.response import Response
import yaml

# запуск worker ов: celery -A core.celery worker

'''Отправляем сообщение при подтверждении заказа - Клиенту'''
@shared_task
def celery_confirmation_order_email(recipient_email, username, order_id, product_infos, address_dict):
    print('yes')
    address_str = f'{address_dict["city"]}, {address_dict["street"]}, ' \
                  f'{address_dict["house"]},{address_dict["building"]}, {address_dict["apartment"]}'
    subject = f'Ваш заказ №. {order_id} подтвержден'

    product_info_str = ""
    for item in product_infos:
        product_info_str += f'\n\nИнформация о заказе:' \
                            f'\nНазвание: {product_infos[item][0]} \nМодель {product_infos[item][1]} \nКоличество: {product_infos[item][2]}  \n' \
                            f'Цена: {product_infos[item][3]}\n'
    message = f'{username}, Ваш заказ подтвержден.\n' \
              f'Details: Номер заказа: {order_id}, {product_info_str}\n' \
              f'Адрес доставки: {address_str}'
    recipient_list = [recipient_email]
    send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list)


'''Отправляем сообщение при подтверждении заказа - Компании'''
@shared_task
def celery_confirmation_order_email_for_shop(dict_order: dict, order_id, address_dict):
    address_str = f'{address_dict["city"]}, {address_dict["street"]}, ' \
                  f'{address_dict["house"]},{address_dict["building"]}, {address_dict["apartment"]}'
    subject = f'В вашем магазине был сделан заказ №. {order_id} - он подтвержден'

    '''Проверяем если список - значит несколько товаров у одного магазина, собираем и отправляем сообщение магазину'''
    for key, value in dict_order.items():
        mess = ''
        if type(value) == list:
            for item in value:
                mess += f'Название продукта - {item[1]} - {item[2]} шт. \n'
            message = f'Заказ подтвержден.\n' \
                          f'Details: Номер заказа: {order_id}, Информация о заказе: \n {mess}' \
                          f'Адрес доставки: {address_str}'

            recipient_list = [key]
            send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER,
                          recipient_list=recipient_list)
        else:
            mess += f'Назавание продукта - {value[1]} - {value[2]} шт. \n'
            message = f'Заказ подтвержден.\n' \
                      f'Details: Номер заказа: {order_id}, Информация о заказе: \n {mess}' \
                      f'Адрес доставки: {address_str}'

            recipient_list = [key]
            send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER,
                      recipient_list=recipient_list)


'''Загружаем продукты - Компании'''
@shared_task
def celery_save_products_shop(filename):
    with open(f"media/{filename}") as stream:
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