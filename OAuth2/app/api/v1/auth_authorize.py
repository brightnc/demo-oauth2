from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.services.auth_service import OAuth2Service
from urllib.parse import urlencode
from app.configs.config import settings

router = APIRouter()

@router.get("")
@router.post("")
async def authorize(
    request: Request,
    client_id: str,
    response_type: str,
    redirect_uri: str,
    scope: str,
    state: str | None = None,
    db: Session = Depends(get_db)
):
    service = OAuth2Service(db)
    
    try:
        # ตรวจสอบว่า user login แล้วหรือยัง
        user_id = request.session.get("user_id")
        if not user_id:
            # ถ้ายังไม่ได้ login ให้ redirect ไปหน้า login พร้อม parameters ทั้งหมด
            params = {
                "client_id": client_id,
                "response_type": response_type,
                "redirect_uri": redirect_uri,
                "scope": scope,
                "state": state
            }
            return RedirectResponse(url=f"{settings.API_V1_STR}/auth/login?{urlencode(params)}")
            
        # Validate response type
        if response_type != "code":
            raise HTTPException(status_code=400, detail="Only authorization code is supported")
        
        # Validate client and redirect URI
        client = service.validate_client(client_id, redirect_uri)
        if not client:
            raise HTTPException(status_code=400, detail="Invalid client_id or redirect_uri")
        
        # Create authorization code
        auth_code = service.create_authorization_code(
            client_id=client_id,
            scope=scope,
            user_id=user_id
        )
        
        # Prepare success response parameters
        params = {
            "code": auth_code,
            "state": state
        }
        
        # Redirect to client with authorization code
        redirect_url = f"{redirect_uri}?{urlencode(params)}"
        return RedirectResponse(url=redirect_url)
        
    except HTTPException as e:
        # Handle errors by redirecting with error parameters
        error_params = {
            "error": e.detail,
            "state": state
        }
        redirect_url = f"{redirect_uri}?{urlencode(error_params)}"
        return RedirectResponse(url=redirect_url)