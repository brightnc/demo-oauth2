# auth_token.py
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import APIRouter, Depends, HTTPException, Form
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.services.auth_service import OAuth2Service
from app.configs.config import settings

router = APIRouter()

security = HTTPBasic()

@router.post("")
async def token(
    code: str = Form(...),
    grant_type: str = Form("authorization_code"),
    redirect_uri: str = Form(...),
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    service = OAuth2Service(db)
    
    # ตรวจสอบ grant_type
    if grant_type != "authorization_code":
        raise HTTPException(status_code=400, detail="Invalid grant type")
    
    # ตรวจสอบ client credentials จาก Basic Auth
    client = service.get_client(credentials.username)
    if not client:
        raise HTTPException(status_code=401, detail="Invalid client credentials")
    
    # ตรวจสอบ redirect URI
    if redirect_uri not in client.redirect_uris.split(','):
        raise HTTPException(status_code=400, detail="Invalid redirect URI")
    
    # ตรวจสอบ code
    token = service.validate_authorization_code(code)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid or expired code")
    
    # ตรวจสอบว่า code นี้เป็นของ client นี้จริงๆ
    if token.client_id != credentials.username:
        raise HTTPException(status_code=400, detail="Code was issued to a different client")
    
    # สร้าง access token และ refresh token
    access_token = service.create_access_token(
        client_id=credentials.username,
        scope=token.scope,
        user_id=token.user_id
    )
    refresh_token = service.create_refresh_token(
        client_id=credentials.username,
        scope=token.scope,
        user_id=token.user_id
    )
    
    # ลบ authorization code หลังจากใช้แล้ว
    service.revoke_token(code)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "scope": token.scope
    }