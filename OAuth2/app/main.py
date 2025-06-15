from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.configs.config import settings
from app.api.v1 import auth_client,auth_authorize,auth_token,auth_login,auth_register
from app.db.session import engine
from app.models import auth_model, user_model  # Import models to ensure they are registered
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.base import Base
from starlette.middleware.sessions import SessionMiddleware
import secrets

# Remove database tables
# Base.metadata.drop_all(bind=engine)
# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# เพิ่ม Session Middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,  # Use the same secret key from settings
    session_cookie="session",
    max_age=3600,
    same_site="lax",
    https_only=False,  # Set to True in production
)

# เพิ่ม CORS Middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_methods=["*"],
        allow_credentials=True,
        allow_headers=["*"],
    )

app.include_router(auth_client.router, prefix=f"{settings.API_V1_STR}/auth/clients")
app.include_router(auth_authorize.router, prefix=f"{settings.API_V1_STR}/auth/authorize")
app.include_router(auth_token.router, prefix=f"{settings.API_V1_STR}/auth/token")
app.include_router(auth_login.router, prefix=f"{settings.API_V1_STR}/auth/login")
app.include_router(auth_register.router, prefix=f"{settings.API_V1_STR}/auth/register")


