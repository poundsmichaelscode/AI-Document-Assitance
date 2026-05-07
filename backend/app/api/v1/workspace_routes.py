from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse
router = APIRouter(prefix='/workspaces', tags=['Workspaces'])
@router.post('', response_model=WorkspaceResponse)
def create_workspace(payload: WorkspaceCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    w = WorkspaceRepository(db).create(current_user.id, payload.name)
    return WorkspaceResponse(id=w.id, name=w.name, owner_id=w.owner_id, created_at=w.created_at)
@router.get('', response_model=list[WorkspaceResponse])
def list_workspaces(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return [WorkspaceResponse(id=w.id, name=w.name, owner_id=w.owner_id, created_at=w.created_at) for w in WorkspaceRepository(db).list_for_owner(current_user.id)]
