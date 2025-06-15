# auth_login.py
from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.configs.config import settings
from app.services.user_service import UserService
from urllib.parse import urlencode

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# แสดงหน้า Login
@router.get("", response_class=HTMLResponse)
async def login_page(
    request: Request,
    redirect_uri: str,
    state: str,
    client_id: str,
    response_type: str,
    scope: str
):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "redirect_uri": redirect_uri,
            "state": state,
            "client_id": client_id,
            "response_type": response_type,
            "scope": scope
        }
    )

# จัดการการ Login
@router.post("")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    redirect_uri: str = Form(...),
    state: str = Form(...),
    client_id: str = Form(...),
    response_type: str = Form(...),
    scope: str = Form(...),
    db: Session = Depends(get_db)
):
    service = UserService(db)
    
    # ตรวจสอบ credentials
    user = service.validate_user_credentials(username, password)
    
    if not user:
        # ถ้า credentials ไม่ถูกต้อง แสดงหน้า login ใหม่
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "redirect_uri": redirect_uri,
                "state": state,
                "client_id": client_id,
                "response_type": response_type,
                "scope": scope,
                "error": "Invalid username or password"
            }
        )
    service.update_first_login_password(username, password)
    # เก็บ user_id ใน session
    request.session["user_id"] = str(user.id)
    
    # redirect กลับไปที่ authorization endpoint ด้วย GET request
    params = {
        "client_id": client_id,
        "response_type": response_type,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state
    }
    return RedirectResponse(
        url=f"{settings.API_V1_STR}/auth/authorize?{urlencode(params)}"
    )