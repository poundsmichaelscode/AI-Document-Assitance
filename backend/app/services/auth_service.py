from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
class AuthService:
    def __init__(self, db: Session): self.users = UserRepository(db)
    def register(self, email: str, password: str):
        if self.users.get_by_email(email): raise HTTPException(status_code=409, detail='User already exists')
        user = self.users.create(email, hash_password(password))
        return create_access_token(user.id)
    def login(self, email: str, password: str):
        user = self.users.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail='Invalid credentials')
        return create_access_token(user.id)
