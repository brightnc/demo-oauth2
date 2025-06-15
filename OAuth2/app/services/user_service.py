from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from uuid import uuid4 as generate_uuid
from datetime import datetime, UTC, timedelta
from app.configs.config import settings
from app.models.user_model import UserCredential
from app.schemas.user_schema import UserRegister, UserRegisterResponse 
from app.utils.password import hash_password,check_password
from fastapi import HTTPException


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def validate_user_credentials(self, username: str, password: str) -> UserCredential:
        user = self.user_repo.find_user(username)
        if not user:
            return None
        password_match = check_password(password, user.password, user.hash_type)
        if not password_match:
            return None
        
        return user
    
    def update_first_login_password(self, username: str, password: str) -> None:
        user = self.user_repo.find_user(username)
        if not user:
            return None
        hashed_password = hash_password(password)
        user.password = hashed_password
        user.hash_type = "bcrypt"
        self.user_repo.update_user(user)
        return user

    def register_user(self, user_data: UserRegister) -> UserRegisterResponse:
        user = self.user_repo.find_user(user_data.username)
        if user: 
            raise HTTPException(status_code=400, detail="Username already exists")
        hashed_password = hash_password(user_data.password)
        user_data.password = hashed_password
        user = self.user_repo.create_user(user_data)
        return UserRegisterResponse(id=str(user.id))
    