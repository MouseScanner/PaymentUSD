import uuid
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.models import Account, Transfer
from app.models.transfer import TransferStatus
from app.schemas.transfer import TransferCreate
from app.services.account_service import AccountService
from app.utils.exceptions import AccountNotFoundError, InsufficientBalanceError
from app.worker import process_transfer_task


class TransferService:
    
    @staticmethod
    def create_transfer(db: Session, transfer_data: TransferCreate) -> Transfer:
        from_account = AccountService.get_account_by_id(db, transfer_data.from_account_id)
        to_account = AccountService.get_account_by_id(db, transfer_data.to_account_id)
        
        if not from_account:
            raise AccountNotFoundError(f"Source account {transfer_data.from_account_id} not found")
        if not to_account:
            raise AccountNotFoundError(f"Destination account {transfer_data.to_account_id} not found")
        
        if from_account.balance < transfer_data.amount:
            raise InsufficientBalanceError("Insufficient balance")
        
        transfer = Transfer(
            external_id=str(uuid.uuid4()),
            from_account_id=transfer_data.from_account_id,
            to_account_id=transfer_data.to_account_id,
            amount=transfer_data.amount,
            status=TransferStatus.PENDING
        )
        
        db.add(transfer)
        db.commit()
        db.refresh(transfer)
        
        # Отправляем задачу в Celery для асинхронной обработки
        process_transfer_task.delay(transfer.id)
        
        return transfer
    
    @staticmethod
    def get_transfer_by_id(db: Session, transfer_id: int) -> Optional[Transfer]:
        return db.query(Transfer).filter(Transfer.id == transfer_id).first()
    
    @staticmethod
    def get_transfer_by_external_id(db: Session, external_id: str) -> Optional[Transfer]:
        return db.query(Transfer).filter(Transfer.external_id == external_id).first()
    
    @staticmethod
    def process_transfer(db: Session, transfer_id: int) -> bool:
        transfer = TransferService.get_transfer_by_id(db, transfer_id)
        if not transfer or transfer.status != TransferStatus.PENDING:
            return False
        
        try:
            transfer.status = TransferStatus.PROCESSING
            db.commit()
            
            # Атомарная транзакция для обновления балансов
            from_account = db.query(Account).filter(Account.id == transfer.from_account_id).with_for_update().first()
            to_account = db.query(Account).filter(Account.id == transfer.to_account_id).with_for_update().first()
            
            if from_account.balance < transfer.amount:
                transfer.status = TransferStatus.FAILED
                transfer.error_message = "Insufficient balance"
                db.commit()
                return False
            
            from_account.balance -= transfer.amount
            to_account.balance += transfer.amount
            transfer.status = TransferStatus.COMPLETED
            
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            transfer.status = TransferStatus.FAILED
            transfer.error_message = str(e)
            db.commit()
            return False 