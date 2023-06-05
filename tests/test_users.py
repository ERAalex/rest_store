import requests
import pytest

# pytest tests/*
#  py.test tests/test_users.py -v -s   - чтобы увидеть ответ с data


def test_equal():
    assert 1 == 1, 'Number is not equal'


def test_call_call_endpoint():
    response = requests.get('http://127.0.0.1:8000/swagger')
    assert response.status_code == 200


ENDPOINT = 'http://127.0.0.1:8000/auth'
pytest.global_variable_JWT_user = ''


'''TEST - User part'''

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
#     response = requests.post(ENDPOINT + '/users/', json=payload)
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


def test_user_contact_create():
    ''' done - working '''

    header = {
        'Authorization': 'JWT ' + pytest.global_variable_JWT_user}

    payload = {
        'city': 'Moscow',
        'street': 'Smolenskaya',
        'house': '23',
        'structure': '',
        'building': '',
        'apartment': '141',
        'phone': '89117861599',
    }

    response = requests.get('http://127.0.0.1:8000' + '/contacts/', headers=header)
    data_id = response.json()


    if response.status_code == 200 and len(data_id) > 0:
        data_id = response.json()[0]['id']
        response = requests.put('http://127.0.0.1:8000' + f'/contacts/{data_id}', json=payload, headers=header)
        assert response.status_code == 200
        data = response.json()
    else:
        response = requests.post('http://127.0.0.1:8000' + '/contacts/', json=payload, headers=header)
        assert response.status_code == 201
        data = response.json()
    print(data)
    return data


# def test_delete_user():
#     ''' done - working '''
#     header = {
#         'Authorization': 'JWT ' + pytest.global_variable_JWT_user}
#
#     payload = {
#         'current_password': "Test007007",
#     }
#
#     response = requests.delete(f'{ENDPOINT}/users/me/', json=payload, headers=header)
#     assert response.status_code == 204

