from langchain_openai import ChatOpenAI
from app.core.config import get_settings
from app.schemas.chat import AskResponse, SourceItem
from app.services.vector_service import VectorService
class RagService:
    def answer(self, workspace_id: str, question: str, top_k: int):
        s = get_settings()
        if not s.openai_api_key or s.openai_api_key.startswith('your_'):
            raise ValueError('Set a real OPENAI_API_KEY in backend/.env')
        matches = VectorService().search(question, workspace_id, top_k)
        if not matches: return AskResponse(answer='I could not find relevant information in the uploaded documents.', sources=[])
        context, sources = [], []
        for doc, score in matches:
            context.append(doc.page_content)
            sources.append(SourceItem(document_id=doc.metadata.get('document_id',''), file_name=doc.metadata.get('file_name','unknown'), page=doc.metadata.get('page'), chunk_index=doc.metadata.get('chunk_index'), score=round(float(score),4) if score is not None else None, snippet=doc.page_content[:500]))
        prompt = f"Answer only using this context. If missing, say it is not in the uploaded documents.\n\nContext:\n{chr(10).join(context)}\n\nQuestion:\n{question}"
        llm = ChatOpenAI(model=s.openai_chat_model, temperature=0, api_key=s.openai_api_key)
        return AskResponse(answer=llm.invoke(prompt).content, sources=sources)
