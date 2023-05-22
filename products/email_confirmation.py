from django.conf import settings
from django.core.mail import send_mail


'''Отправляем сообщение'''

def confirmation_order_email(recipient_email, username, order_id, product_infos, address_dict):
    address_str = f'{address_dict["city"]}, {address_dict["street"]}, ' \
                  f'{address_dict["house"]},{address_dict["building"]}, {address_dict["apartment"]}'
    subject = f'Ваш заказ Nr. {order_id} подтвержден'

    product_info_str = ""
    for item in product_infos:
        product_info_str += f'Информация о заказе:' \
                            f'\nНазвание: {product_infos[item][0]} \nМодель {product_infos[item][1]} \nКоличество: {product_infos[item][2]}  \n' \
                            f'Цена: {product_infos[item][3]}'
    message = f'{username}, Ваш заказ подтвержден.\n' \
              f'Details: Номер заказа: {order_id}, {product_info_str}\n' \
              f'Адрес доставки: {address_str}'
    recipient_list = [recipient_email]
    send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipient_list)

