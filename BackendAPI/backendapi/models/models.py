from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    registry,
    relationship,
)

table_registry = registry()


@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    cpf: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    accounts: Mapped[list['BankAccount']] = relationship(
        back_populates='user',
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )


@mapped_as_dataclass(table_registry)
class BankAccount:
    __tablename__ = 'bank_account'
    account_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='accounts', init=False)
    balance: Mapped[float]
    transactions: Mapped[list['Transaction']] = relationship(
        back_populates='account', cascade='all, delete-orphan', init=False
    )


class TransactionType(str, Enum):
    deposit = 'deposit'
    withdrawal = 'withdrawal'


@mapped_as_dataclass(table_registry)
class Transaction:
    __tablename__ = 'transaction'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey('bank_account.account_id')
    )
    type_transaction: Mapped[TransactionType]
    amount: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    account: Mapped['BankAccount'] = relationship(
        back_populates='transactions', init=False
    )
