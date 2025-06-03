from celery import Celery

from app.config import settings
from app.database import SessionLocal
from app.services.transfer_service import TransferService

celery_app = Celery(
    "payment_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def process_transfer_task(self, transfer_id: int):
    db = SessionLocal()
    try:
        success = TransferService.process_transfer(db, transfer_id)
        if not success:
            raise Exception(f"Failed to process transfer {transfer_id}")
        return {"status": "completed", "transfer_id": transfer_id}
    except Exception as exc:
        db.rollback()
        raise self.retry(exc=exc, countdown=60)
    finally:
        db.close() 