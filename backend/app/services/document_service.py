from datetime import datetime
from pathlib import Path
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.repositories.document_repository import DocumentRepository
from app.repositories.workspace_repository import WorkspaceRepository
from app.services.storage_service import StorageService
from app.workers.tasks import ingest_document_task
class DocumentService:
    def __init__(self, db: Session):
        self.docs = DocumentRepository(db); self.workspaces = WorkspaceRepository(db); self.storage = StorageService()
    async def upload(self, user_id: str, workspace_id: str, file: UploadFile):
        if not self.workspaces.get_owned(workspace_id, user_id): raise HTTPException(status_code=404, detail='Workspace not found')
        content = await file.read(); s = get_settings()
        ext = Path(file.filename or '').suffix.lower().replace('.', '')
        if ext not in s.allowed_extensions_list: raise HTTPException(status_code=400, detail='Unsupported file type')
        if len(content) > s.max_upload_size_mb * 1024 * 1024: raise HTTPException(status_code=413, detail='File too large')
        safe_name = Path(file.filename or 'document').name
        key = f"{workspace_id}/{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{safe_name}"
        doc = self.docs.create(workspace_id, user_id, safe_name, ext, self.storage.upload_bytes(content, key))
        ingest_document_task.delay(doc.id)
        return doc
