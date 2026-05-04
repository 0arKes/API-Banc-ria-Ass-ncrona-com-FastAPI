import pytest
from sqlalchemy import select

from backendapi.models.models import BankAccount, User


@pytest.mark.asyncio
async def test_create_user(session):
    new_user = User(email='test@test.com', password='123456', cpf=1)
    session.add(new_user)
    await session.commit()

    get_user = await session.scalar(select(User).where(User.cpf == 1))

    assert get_user.email == 'test@test.com'


@pytest.mark.asyncio
async def test_create_bank_account(session, user_test):
    bank_account = BankAccount(
        owner_id=user_test.id,
        balance=100,
    )
    session.add(bank_account)
    await session.commit()
    test = await session.scalar(select(BankAccount))
    assert test.account_id == 1
