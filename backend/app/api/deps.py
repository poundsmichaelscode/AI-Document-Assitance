from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.core.security import decode_token
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
bearer = HTTPBearer(auto_error=False)
def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)):
    if not credentials: raise HTTPException(status_code=401, detail='Authentication required')
    try: payload = decode_token(credentials.credentials)
    except ValueError: raise HTTPException(status_code=401, detail='Invalid token')
    user = UserRepository(db).get_by_id(payload.get('sub'))
    if not user: raise HTTPException(status_code=401, detail='User not found')
    return user
