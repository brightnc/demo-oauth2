from fastapi import APIRouter, Depends, HTTPException, Request, Response, Form
from app.db.session import get_db
from app.schemas.auth import OAuth2ClientResponse, OAuth2ClientCreate
from sqlalchemy.orm import Session
from app.services.auth_service import OAuth2Service

router = APIRouter()

@router.post("", response_model=OAuth2ClientResponse)
def create_client( client_data: OAuth2ClientCreate,db: Session = Depends(get_db)):
    service = OAuth2Service(db)
    return service.create_client(client_data)

