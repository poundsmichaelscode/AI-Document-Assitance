from datetime import datetime
from pydantic import BaseModel
class DocumentResponse(BaseModel):
    id: str
    workspace_id: str
    file_name: str
    file_type: str
    status: str
    page_count: int | None = None
    error_message: str | None = None
    created_at: datetime
