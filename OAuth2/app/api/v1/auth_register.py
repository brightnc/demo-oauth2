from fastapi import APIRouter, Depends, HTTPException, Request, Response, Form
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.schemas.user_schema import UserRegister, UserRegisterResponse

router = APIRouter()

@router.post("", response_model=UserRegisterResponse)
def register_user( user_data: UserRegister,db: Session = Depends(get_db)):
    service = UserService(db)
    return service.register_user(user_data)

