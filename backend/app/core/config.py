from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = 'AI Document Assistant API'
    app_env: str = 'development'
    debug: bool = True
    api_v1_prefix: str = '/api/v1'

    openai_api_key: str = ''
    openai_chat_model: str = 'gpt-4o-mini'
    openai_embedding_model: str = 'text-embedding-3-small'
    openai_embedding_dimensions: int = 1536

    pinecone_api_key: str = ''
    pinecone_index_name: str = 'doc-assistant'
    pinecone_cloud: str = 'aws'
    pinecone_region: str = 'us-east-1'

    database_url: str
    redis_url: str

    jwt_secret_key: str
    jwt_algorithm: str = 'HS256'
    access_token_expire_minutes: int = 1440

    max_upload_size_mb: int = 25
    allowed_file_extensions: str = 'pdf,docx,txt'
    chunk_size: int = 1200
    chunk_overlap: int = 200
    retrieval_top_k: int = 5
    cors_origins: str = 'http://localhost:5173'

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False, extra='ignore')

    @property
    def allowed_extensions_list(self) -> list[str]:
        return [item.strip().lower() for item in self.allowed_file_extensions.split(',') if item.strip()]

    @property
    def cors_origins_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(',') if item.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()
