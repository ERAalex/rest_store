import requests
import pytest

# pytest tests/*
# python -m pytest -v -s    - чтобы увидеть ответ с data



def test_equal():
    assert 1 == 1, 'Number is not equal'


def test_call_call_endpoint():
    response = requests.get('http://127.0.0.1:8000/swagger')
    assert response.status_code == 200


ENDPOINT = 'http://127.0.0.1:8000/auth'
pytest.global_variable_JWT_user = ''

@pytest.fixture
def test_get_admin_JWT():
    payload = {
        'email': 'eraspb@mail.ru',
        'password': 'Naz'
    }

    response = requests.post('http://127.0.0.1:8000/auth/jwt/create', json=payload)
    assert response.status_code == 200

    data = response.json()
    token_admin = data['access']
    print(token_admin)
    return token_admin


'''TEST - User part'''
#
# Пользователь создается, но тест зависает т.к. идет попытка отправить письмо в тесте smtplib.SMTPServerDisconnected
# def test_user_create():
#     payload = {
#         'name': 'samuel',
#         'person_telephone': '89117861595',
#         'surname': 'lesli',
#         'email': 'eraspbb@mail.ru',
#         'password': 'Nazca1221',
#         're_password': 'Nazca1221'
#     }
#
#     response = requests.post(ENDPOINT + 'users/', json=payload)
#     assert response.status_code == 201
#     data = response.json()
#     print(data)
#     return data['id']


def test_user_get_Jwt():
    ''' done - working '''

    payload = {
        'email': "eraspbb@mail.ru",
        'password': "Nazca1221",
    }

    response = requests.post(
        f"{ENDPOINT}/jwt/create", json=payload)

    assert response.status_code == 200
    data = response.json()
    print(data)
    print(data['access'])
    pytest.global_variable_JWT_user = data['access']
    return pytest.global_variable_JWT_user


def test_user_get_user():
    ''' done - working '''
    header = {
        'Authorization': 'JWT ' + pytest.global_variable_JWT_user}

    response = requests.get(f'{ENDPOINT}/users/me/', headers=header)
    assert response.status_code == 200
    data = response.json()
    print(data)


def test_delete_user():
    ''' done - working '''
    header = {
        'Authorization': 'JWT ' + pytest.global_variable_JWT_user}

    response = requests.delete(f'{ENDPOINT}/users/me', headers=header)
    assert response.status_code == 204


'''Partner part Test'''
# def test_upload():
#
