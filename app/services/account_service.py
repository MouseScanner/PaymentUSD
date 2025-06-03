from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Account
from app.schemas.account import AccountCreate, AccountResponse
from app.utils.exceptions import AccountAlreadyExistsError, AccountNotFoundError


class AccountService:
    
    @staticmethod
    def create_account(db: Session, account_data: AccountCreate) -> Account:
        try:
            account = Account(external_id=account_data.external_id)
            db.add(account)
            db.commit()
            db.refresh(account)
            return account
        except IntegrityError:
            db.rollback()
            raise AccountAlreadyExistsError(f"Account with external_id {account_data.external_id} already exists")
    
    @staticmethod
    def get_account_by_id(db: Session, account_id: int) -> Optional[Account]:
        return db.query(Account).filter(Account.id == account_id, Account.is_active == True).first()
    
    @staticmethod
    def get_account_by_external_id(db: Session, external_id: str) -> Optional[Account]:
        return db.query(Account).filter(Account.external_id == external_id, Account.is_active == True).first()
    
    @staticmethod
    def deactivate_account(db: Session, account_id: int) -> bool:
        account = AccountService.get_account_by_id(db, account_id)
        if not account:
            raise AccountNotFoundError(f"Account {account_id} not found")
        
        account.is_active = False
        db.commit()
        return True 