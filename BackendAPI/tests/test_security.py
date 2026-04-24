from http import HTTPStatus

from jwt import decode

from backendapi.security import creat_access_token
from backendapi.settings import Settings


def test_jwt():
    data = {'test': 'test'}
    token = creat_access_token(data=data)

    decoded = decode(token, Settings().SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_token(client, user_test):
    response = client.post(
        '/token',
        data={
            'username': user_test.email,
            'password': user_test.clean_password,
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_invalid_token(client):
    response = client.delete(
        '/user/1', headers={'Authorization': 'Bearer test'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
