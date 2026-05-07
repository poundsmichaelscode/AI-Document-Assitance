from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.repositories.document_repository import DocumentRepository
from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService
router = APIRouter(prefix='/documents', tags=['Documents'])
def serialize(d): return DocumentResponse(id=d.id, workspace_id=d.workspace_id, file_name=d.file_name, file_type=d.file_type, status=d.status, page_count=d.page_count, error_message=d.error_message, created_at=d.created_at)
@router.post('/upload', response_model=DocumentResponse)
async def upload_document(workspace_id: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return serialize(await DocumentService(db).upload(current_user.id, workspace_id, file))
@router.get('', response_model=list[DocumentResponse])
def list_documents(workspace_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not WorkspaceRepository(db).get_owned(workspace_id, current_user.id): raise HTTPException(status_code=404, detail='Workspace not found')
    return [serialize(d) for d in DocumentRepository(db).list_for_workspace(workspace_id)]
