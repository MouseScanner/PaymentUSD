import json
import traceback
from tornado.web import RequestHandler
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.utils.exceptions import PaymentAPIException


class BaseHandler(RequestHandler):
    
    def prepare(self):
        self.db: Session = SessionLocal()
    
    def on_finish(self):
        self.db.close()
    
    def write_error(self, status_code, **kwargs):
        if "exc_info" in kwargs:
            exc_type, exc_value, exc_traceback = kwargs["exc_info"]
            
            if isinstance(exc_value, PaymentAPIException):
                self.set_status(400)
                self.write({"error": str(exc_value)})
            else:
                self.set_status(500)
                self.write({"error": "Internal server error"})
        else:
            self.write({"error": "Unknown error"})
    
    def get_json_body(self):
        try:
            return json.loads(self.request.body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise ValueError("Invalid JSON in request body")
    
    def write_json(self, data):
        self.set_header("Content-Type", "application/json")
        if hasattr(data, 'dict'):
            self.write(data.dict())
        else:
            self.write(data) 