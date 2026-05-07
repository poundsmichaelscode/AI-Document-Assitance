from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService
router = APIRouter(prefix='/auth', tags=['Auth'])
@router.post('/register', response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)): return TokenResponse(access_token=AuthService(db).register(payload.email, payload.password))
@router.post('/login', response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)): return TokenResponse(access_token=AuthService(db).login(payload.email, payload.password))
@router.get('/me', response_model=UserResponse)
def me(current_user=Depends(get_current_user)): return UserResponse(id=current_user.id, email=current_user.email)
