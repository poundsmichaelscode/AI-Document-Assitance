from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.chat import AskRequest, AskResponse
from app.services.rag_service import RagService
router = APIRouter(prefix='/chat', tags=['Chat'])
@router.post('/ask', response_model=AskResponse)
def ask(payload: AskRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not WorkspaceRepository(db).get_owned(payload.workspace_id, current_user.id): raise HTTPException(status_code=404, detail='Workspace not found')
    return RagService().answer(payload.workspace_id, payload.question, payload.top_k)
