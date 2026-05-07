from sqlalchemy.orm import Session
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.services.document_parser import DocumentParserService
from app.services.storage_service import StorageService
from app.services.vector_service import VectorService
class IngestionService:
    def __init__(self, db: Session):
        self.db = db; self.repo = DocumentRepository(db); self.storage = StorageService(); self.parser = DocumentParserService()
        s = get_settings(); self.splitter = RecursiveCharacterTextSplitter(chunk_size=s.chunk_size, chunk_overlap=s.chunk_overlap)
    def ingest(self, document_id: str):
        doc = self.db.query(Document).filter(Document.id == document_id).first()
        if not doc: raise ValueError('Document not found')
        self.repo.mark_processing(document_id)
        try:
            pages = self.parser.parse(self.storage.resolve_local_path(doc.storage_key), doc.file_type, doc.file_name)
            chunks = self.splitter.split_documents(pages)
            for i, chunk in enumerate(chunks):
                chunk.metadata.update({'document_id': doc.id, 'workspace_id': doc.workspace_id, 'file_name': doc.file_name, 'chunk_index': i})
            VectorService().add_documents(chunks)
            self.repo.mark_ready(document_id, max((p.metadata.get('page', 1) for p in pages), default=1))
        except Exception as exc:
            self.repo.mark_failed(document_id, str(exc)); raise
def ingest_document_sync(document_id: str):
    db = SessionLocal()
    try: IngestionService(db).ingest(document_id)
    finally: db.close()
