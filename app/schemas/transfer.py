from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, validator

from app.models.transfer import TransferStatus
from app.config import settings


class TransferCreate(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: Decimal
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        if v < Decimal(str(settings.MIN_TRANSFER_AMOUNT)):
            raise ValueError(f'Amount must be at least {settings.MIN_TRANSFER_AMOUNT} USDT')
        return v
    
    @validator('to_account_id')
    def validate_different_accounts(cls, v, values):
        if 'from_account_id' in values and v == values['from_account_id']:
            raise ValueError('Cannot transfer to the same account')
        return v


class TransferResponse(BaseModel):
    id: int
    external_id: str
    from_account_id: int
    to_account_id: int
    amount: Decimal
    status: TransferStatus
    error_message: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True 