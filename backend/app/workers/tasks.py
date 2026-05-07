from app.services.ingestion_service import ingest_document_sync
from app.workers.celery_app import celery_app
@celery_app.task(name='app.workers.tasks.ingest_document_task')
def ingest_document_task(document_id: str): ingest_document_sync(document_id)
