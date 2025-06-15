from sqlalchemy.orm import Session
from app.repositories.auth_repository import OAuth2Repository
from app.repositories.user_repository import UserRepository
from uuid import uuid4 as generate_uuid
from app.schemas.auth import OAuth2ClientResponse, OAuth2ClientCreate
from app.models.auth_model import OAuth2Client, OAuth2Token, TokenType
from datetime import datetime, UTC, timedelta
from app.configs.config import settings
import hashlib


class OAuth2Service:
    def __init__(self, db: Session):
        self.db = db
        self.auth_repo = OAuth2Repository(db)
        self.user_repo = UserRepository(db)

    def create_client(self, client_data: OAuth2ClientCreate) -> OAuth2ClientResponse:
        client_id = generate_uuid()
        client_secret = generate_uuid()
        return self.auth_repo.create_client(
            client_id=client_id,
            client_secret=client_secret,
            **client_data.model_dump()
        )

    def validate_client(self, client_id: str, redirect_uri: str) -> OAuth2Client:
        client = self.auth_repo.get_client(client_id)
        if not client:
            return None
        
        # Check if redirect URI is allowed
        if redirect_uri not in client.redirect_uris.split(','):
            return None
            
        return client
    
    def validate_authorization_code(self, code: str) -> OAuth2Token:
        token = self.auth_repo.find_authorization_code(code)
        if not token:
            return None
        
        # Ensure both datetimes are timezone-aware
        current_time = datetime.now(UTC)
        if token.expires_at.tzinfo is None:
            token.expires_at = token.expires_at.replace(tzinfo=UTC)
        
        if token.expires_at < current_time or token.revoked:
            return None
        
        return token
    
    def create_authorization_code(self, client_id: str, scope: str, user_id: str) -> str:
        code = generate_uuid()
        expires_at = datetime.now(UTC) + timedelta(minutes=10)
        
        token = self.auth_repo.create_token(
            token_type=TokenType.AUTHORIZATION_CODE,
            client_id=client_id,
            scope=scope,
            token=code,
            expires_at=expires_at,
            user_id=user_id
        )
        
        return token.token

    def create_access_token(self, client_id: str, scope: str, user_id: str) -> str:
        access_token = generate_uuid()
        expires_at = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        token = self.auth_repo.create_token(
            token_type=TokenType.ACCESS,
            client_id=client_id,
            scope=scope,
            token=access_token,
            expires_at=expires_at,
            user_id=user_id
        )
        
        return token.token

    def create_refresh_token(self, client_id: str, scope: str, user_id: str) -> str:
        refresh_token = generate_uuid()
        expires_at = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        token = self.auth_repo.create_token(
            token_type=TokenType.REFRESH,
            client_id=client_id,
            scope=scope,
            token=refresh_token,
            expires_at=expires_at,
            user_id=user_id
        )
        
        return token.token

    def get_client(self, client_id: str) -> OAuth2ClientResponse:
        return self.auth_repo.get_client(client_id)
    
    def revoke_token(self, token: str) -> None:
        self.auth_repo.revoke_token(token)