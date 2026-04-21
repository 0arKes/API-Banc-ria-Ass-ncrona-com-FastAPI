from http import HTTPStatus


def test_home(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'msg': 'teste'}


def test_create_user(client):
    response = client.post(
        '/user/',
        json={
            'email': 'alice@example.com',
            'password': 'secret',
            'cpf': 1234567890,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@example.com',
    }


def test_read_user(client):
    response = client.get('/user/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'email': 'alice@example.com',
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/user/1',
        json={
            'email': 'super@gmail.com',
            'password': '123',
            'cpf': 123,
        },
    )
    assert response.status_code == HTTPStatus.OK


def test_delete_user(client):
    response = client.delete('/user/1')
    assert response.status_code == HTTPStatus.OK
