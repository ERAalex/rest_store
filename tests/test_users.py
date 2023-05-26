import requests
import pytest

# pytest tests/*
# python -m pytest -v -s    - чтобы увидеть ответ с data



def test_equal():
    assert 1 == 1, 'Number is not equal'


def test_call_call_endpoint():
    response = requests.get('http://127.0.0.1:8000/swagger')
    assert response.status_code == 200


ENDPOINT = 'http://127.0.0.1:8000/auth/'

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
    return token_admin


# def test_create_user():
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


# def test_get_user():
#     header = {
#         'Authorization': 'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg1MTAwMzk2LCJpYXQiOjE2ODUwOTY3OTYsImp0aSI6IjRmM2ZkN2UzNzMyZDQzNWQ4NWQ4ZGYyZTgwZGNjNjEzIiwidXNlcl9pZCI6Nn0.66dqGLQar8y_9751xAJggBtulipDPytjCEOZyfAR428'}
#
#     response = requests.get('http://127.0.0.1:8000/auth/users/36/', headers=header)
#     assert response.status_code == 200
#     data = response.json()
#     print(data)

#
# def test_delete_user():
#     header = {
#         'Authorization': 'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg1MTAwMzk2LCJpYXQiOjE2ODUwOTY3OTYsImp0aSI6IjRmM2ZkN2UzNzMyZDQzNWQ4NWQ4ZGYyZTgwZGNjNjEzIiwidXNlcl9pZCI6Nn0.66dqGLQar8y_9751xAJggBtulipDPytjCEOZyfAR428'}
#
#     payload = {
#         'current_password': 'Nazca007'
#     }
#     response = requests.delete('http://127.0.0.1:8000/auth/users/36/', json=payload, headers=header)
#     assert response.status_code == 204
#     data = response.json()
#     print(data)