from datetime import datetime

from pydantic import BaseModel

from backendapi.models.models import TransactionType


class TransactionSchema(BaseModel):
    account_id: int
    type_transaction: TransactionType
    amount: float


class TransactionPublicSchema(TransactionSchema):
    created_at: datetime


class TransactionPublicListSchema(BaseModel):
    transactions: list[TransactionPublicSchema]
