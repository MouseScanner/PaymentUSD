from pydantic import ValidationError

from app.handlers.base_handler import BaseHandler
from app.schemas.account import AccountCreate, AccountResponse
from app.services import AccountService
from app.utils.exceptions import AccountNotFoundError


class AccountHandler(BaseHandler):
    
    def post(self):
        """Создание нового аккаунта"""
        try:
            body = self.get_json_body()
            account_data = AccountCreate(**body)
            
            account = AccountService.create_account(self.db, account_data)
            response = AccountResponse.from_orm(account)
            
            self.set_status(201)
            self.write_json(response)
            
        except ValidationError as e:
            self.set_status(400)
            self.write({"error": "Validation error", "details": e.errors()})
    
    def get(self, account_id: str):
        """Получение информации об аккаунте"""
        try:
            account_id = int(account_id)
            account = AccountService.get_account_by_id(self.db, account_id)
            
            if not account:
                raise AccountNotFoundError(f"Account {account_id} not found")
            
            response = AccountResponse.from_orm(account)
            self.write_json(response)
            
        except ValueError:
            self.set_status(400)
            self.write({"error": "Invalid account ID"})


class AccountListHandler(BaseHandler):
    
    def post(self):
        """Создание нового аккаунта (альтернативный endpoint)"""
        return AccountHandler.post(self) 