from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_create_account(client, token):
    response = client.post(
        '/bank/',
        json={'balance': 100},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_create_with_negative_balance(client, token):
    response = client.post(
        '/bank/',
        json={'balance': -100},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_create_with_no_token(client):
    response = client.post(
        '/bank/',
        json={'balance': -100},
        headers={'Authorization': 'Bearer test'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
