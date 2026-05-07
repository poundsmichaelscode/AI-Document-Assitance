from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from app.api.v1.auth_routes import router as auth_router
from app.api.v1.workspace_routes import router as workspace_router
from app.api.v1.document_routes import router as document_router
from app.api.v1.chat_routes import router as chat_router
from app.core.config import get_settings
from app.db.session import Base, engine
import app.models
settings = get_settings()
app = FastAPI(title=settings.app_name, version='1.0.0', default_response_class=ORJSONResponse)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins_list, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
Base.metadata.create_all(bind=engine)
app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(workspace_router, prefix=settings.api_v1_prefix)
app.include_router(document_router, prefix=settings.api_v1_prefix)
app.include_router(chat_router, prefix=settings.api_v1_prefix)
@app.get('/health')
def health(): return {'status': 'ok'}
