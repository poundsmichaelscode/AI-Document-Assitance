from sqlalchemy.orm import Session
from app.models.workspace import Workspace
class WorkspaceRepository:
    def __init__(self, db: Session): self.db = db
    def create(self, owner_id: str, name: str):
        workspace = Workspace(owner_id=owner_id, name=name.strip())
        self.db.add(workspace); self.db.commit(); self.db.refresh(workspace)
        return workspace
    def list_for_owner(self, owner_id: str):
        return self.db.query(Workspace).filter(Workspace.owner_id == owner_id).order_by(Workspace.created_at.desc()).all()
    def get_owned(self, workspace_id: str, owner_id: str):
        return self.db.query(Workspace).filter(Workspace.id == workspace_id, Workspace.owner_id == owner_id).first()
