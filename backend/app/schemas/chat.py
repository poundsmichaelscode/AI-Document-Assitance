from pydantic import BaseModel, Field
class AskRequest(BaseModel):
    workspace_id: str
    question: str = Field(min_length=3)
    top_k: int = Field(default=5, ge=1, le=15)
class SourceItem(BaseModel):
    document_id: str
    file_name: str
    page: int | None = None
    chunk_index: int | None = None
    score: float | None = None
    snippet: str
class AskResponse(BaseModel):
    answer: str
    sources: list[SourceItem]
