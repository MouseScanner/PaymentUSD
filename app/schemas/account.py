from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, validator


class AccountCreate(BaseModel):
    external_id: str
    
    @validator('external_id')
    def validate_external_id(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('external_id cannot be empty')
        if len(v) > 255:
            raise ValueError('external_id too long')
        return v.strip()


class AccountResponse(BaseModel):
    id: int
    external_id: str
    balance: Decimal
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True 