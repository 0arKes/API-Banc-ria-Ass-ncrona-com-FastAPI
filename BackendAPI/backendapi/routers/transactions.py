from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backendapi.database import create_session
from backendapi.models.models import BankAccount, Transaction, User
from backendapi.schemas.transactions_schemas import (
    TransactionPublicListSchema,
    TransactionPublicSchema,
    TransactionSchema,
)
from backendapi.schemas.utility_schemas import FilterPage
from backendapi.security import get_current_user

router = APIRouter(prefix='/transaction', tags=['transaction'])


GetSession = Annotated[AsyncSession, Depends(create_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=TransactionPublicSchema
)
async def create_transaction(
    data: TransactionSchema,
    user: CurrentUser,
    session: GetSession,
):
    account = await session.get(BankAccount, data.account_id)
    if not account:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail='Account not found! go to /bank'
        )
    if account.owner_id != user.id:
        raise HTTPException(
            HTTPStatus.FORBIDDEN, detail="you don't have access"
        )

    if data.type_transaction == 'deposit':
        account.balance += data.amount

    elif data.type_transaction == 'withdrawal':
        if account.balance < data.amount:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, detail='Insufficient balance'
            )

        account.balance -= data.amount

    transaction = Transaction(
        account_id=data.account_id,
        type_transaction=data.type_transaction,
        amount=data.amount,
    )

    session.add(transaction)

    await session.commit()
    await session.refresh(transaction)

    return transaction


@router.get(
    '/', status_code=HTTPStatus.OK, response_model=TransactionPublicListSchema
)
async def read_transactions(
    session: GetSession, filter_page: Annotated[FilterPage, Query()]
):
    query = await session.scalars(
        select(Transaction).offset(filter_page.offset).limit(filter_page.limit)
    )
    transactions = query.all()
    return {'transactions': transactions}
