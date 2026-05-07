from sqlalchemy.orm import Session
from app.models.document import Document
class DocumentRepository:
    def __init__(self, db: Session): self.db = db
    def create(self, workspace_id: str, uploaded_by: str, file_name: str, file_type: str, storage_key: str):
        doc = Document(workspace_id=workspace_id, uploaded_by=uploaded_by, file_name=file_name, file_type=file_type, storage_key=storage_key)
        self.db.add(doc); self.db.commit(); self.db.refresh(doc)
        return doc
    def list_for_workspace(self, workspace_id: str):
        return self.db.query(Document).filter(Document.workspace_id == workspace_id).order_by(Document.created_at.desc()).all()
    def mark_processing(self, document_id: str):
        doc = self.db.query(Document).filter(Document.id == document_id).first()
        if doc: doc.status = 'processing'; self.db.commit()
    def mark_ready(self, document_id: str, page_count: int | None = None):
        doc = self.db.query(Document).filter(Document.id == document_id).first()
        if doc: doc.status = 'ready'; doc.page_count = page_count; doc.error_message = None; self.db.commit()
    def mark_failed(self, document_id: str, error: str):
        doc = self.db.query(Document).filter(Document.id == document_id).first()
        if doc: doc.status = 'failed'; doc.error_message = error[:4000]; self.db.commit()
