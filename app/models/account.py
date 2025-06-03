from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(255), unique=True, index=True, nullable=False)
    balance = Column(Numeric(18, 6), default=Decimal('0'), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    sent_transfers = relationship("Transfer", foreign_keys="Transfer.from_account_id", back_populates="from_account")
    received_transfers = relationship("Transfer", foreign_keys="Transfer.to_account_id", back_populates="to_account") 