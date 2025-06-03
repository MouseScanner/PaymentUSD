from pydantic import ValidationError

from app.handlers.base_handler import BaseHandler
from app.schemas.transfer import TransferCreate, TransferResponse
from app.services import TransferService
from app.utils.exceptions import TransferNotFoundError


class TransferHandler(BaseHandler):
    
    def post(self):
        """Создание нового перевода"""
        try:
            body = self.get_json_body()
            transfer_data = TransferCreate(**body)
            
            transfer = TransferService.create_transfer(self.db, transfer_data)
            response = TransferResponse.from_orm(transfer)
            
            self.set_status(201)
            self.write_json(response)
            
        except ValidationError as e:
            self.set_status(400)
            self.write({"error": "Validation error", "details": e.errors()})
    
    def get(self, transfer_id: str):
        """Получение информации о переводе"""
        try:
            transfer_id = int(transfer_id)
            transfer = TransferService.get_transfer_by_id(self.db, transfer_id)
            
            if not transfer:
                raise TransferNotFoundError(f"Transfer {transfer_id} not found")
            
            response = TransferResponse.from_orm(transfer)
            self.write_json(response)
            
        except ValueError:
            self.set_status(400)
            self.write({"error": "Invalid transfer ID"})


class TransferListHandler(BaseHandler):
    
    def post(self):
        """Создание нового перевода (альтернативный endpoint)"""
        return TransferHandler.post(self) 