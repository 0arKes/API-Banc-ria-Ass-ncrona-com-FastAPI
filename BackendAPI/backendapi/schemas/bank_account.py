from pydantic import BaseModel

from backendapi.schemas.transactions_schemas import TransactionPublicSchema


class CreateAccount(BaseModel):
    balance: float


class AccountPublic(BaseModel):
    account_id: int


class AccountExtract(BaseModel):
    balance: float
    transactions: list[TransactionPublicSchema]
