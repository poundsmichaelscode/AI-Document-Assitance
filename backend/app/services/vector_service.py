import time
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from app.core.config import get_settings
class VectorService:
    def __init__(self):
        self.settings = get_settings()
        if not self.settings.pinecone_api_key or self.settings.pinecone_api_key.startswith('your_'):
            raise ValueError('Set a real PINECONE_API_KEY in backend/.env')
        if not self.settings.openai_api_key or self.settings.openai_api_key.startswith('your_'):
            raise ValueError('Set a real OPENAI_API_KEY in backend/.env')
        self.pc = Pinecone(api_key=self.settings.pinecone_api_key)
        self.embeddings = OpenAIEmbeddings(model=self.settings.openai_embedding_model, dimensions=self.settings.openai_embedding_dimensions, api_key=self.settings.openai_api_key)
        self.ensure_index()
    def ensure_index(self):
        names = [idx['name'] for idx in self.pc.list_indexes()]
        if self.settings.pinecone_index_name not in names:
            self.pc.create_index(name=self.settings.pinecone_index_name, dimension=self.settings.openai_embedding_dimensions, metric='cosine', spec=ServerlessSpec(cloud=self.settings.pinecone_cloud, region=self.settings.pinecone_region), deletion_protection='disabled')
            time.sleep(3)
    def store(self):
        return PineconeVectorStore(index_name=self.settings.pinecone_index_name, embedding=self.embeddings)
    def add_documents(self, docs):
        if docs: self.store().add_documents(docs)
    def search(self, query: str, workspace_id: str, k: int):
        return self.store().similarity_search_with_relevance_scores(query=query, k=k, filter={'workspace_id': {'$eq': workspace_id}})
