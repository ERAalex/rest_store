import requests
import pytest
from pprint import pprint

# pytest tests/*

# py.test tests/test_products.py -v -s - чтобы увидеть ответ с data


def test_equal():
    assert 1 == 1, 'Number is not equal'


def test_call_call_endpoint():
    response = requests.get('http://127.0.0.1:8000/swagger')
    assert response.status_code == 200


ENDPOINT_USER = 'http://127.0.0.1:8000/auth'
ENDPOINT_PRODUCT = 'http://127.0.0.1:8000/products'
pytest.global_variable_JWT_user = ''
pytest.global_variable_some_id_product = ''

'''TEST - Product part'''
''' Create and use some User - to use it in tests, i will use eraspb@mail.ru'''


# def test_user_create():
#     ''' done - working '''
#
#     payload = {
#         'name': 'John',
#         'person_telephone': '89117861595',
#         'surname': 'Snow',
#         'email': 'eraspb@mail.ru',
#         'password': 'Test007007',
#         're_password': 'Test007007',
#     }
#
#     response = requests.post(ENDPOINT_USER + '/users/', json=payload)
#     assert response.status_code == 201
#     data = response.json()
#     print(data)
#     return data['id']


def test_user_get_Jwt():
    ''' done - working '''

    payload = {
        'email': "eraspb@mail.ru",
        'password': "Test007007",
    }

    response = requests.post(
        f"{ENDPOINT_USER}/jwt/create", json=payload)

    assert response.status_code == 200
    data = response.json()
    print(data['access'])
    pytest.global_variable_JWT_user = data['access']
    return pytest.global_variable_JWT_user


def test_product_get():
    ''' done - working '''

    header = {
            'Authorization': 'JWT ' + pytest.global_variable_JWT_user}
    response = requests.get(ENDPOINT_PRODUCT, headers=header)
    assert response.status_code == 200
    data = response.json()
    pytest.global_variable_some_id_product = data[0]['products'][0]['id']
    return data


def test_product_get_by_id():
    ''' done - working '''

    header = {
            'Authorization': 'JWT ' + pytest.global_variable_JWT_user}
    response = requests.get(ENDPOINT_PRODUCT + f'/{pytest.global_variable_some_id_product }', headers=header)
    assert response.status_code == 200
    data = response.json()
    print(data)
    return data



def test_shop_get():
    ''' done - working '''

    header = {
            'Authorization': 'JWT ' + pytest.global_variable_JWT_user}
    response = requests.get('http://127.0.0.1:8000/shops', headers=header)
    assert response.status_code == 200
    data = response.json()
    print(data)
    return data
