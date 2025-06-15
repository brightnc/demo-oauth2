from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum as SQLEnum, UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime, UTC
from app.models.user_model import UserCredential, UserRole
import enum
from uuid import uuid4
class TokenType(str, enum.Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    BEARER = "bearer"
    AUTHORIZATION_CODE = "authorization_code"

class TokenStatus(str, enum.Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"



class OAuth2Client(Base):
    __tablename__ = "oauth2_clients"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    client_id = Column(String, unique=True, index=True, nullable=False)
    client_secret = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    redirect_uris = Column(String)  # Comma-separated list of URIs
    grant_types = Column(String)    # Comma-separated list of grant types
    response_types = Column(String) # Comma-separated list of response types
    scope = Column(String)
    token_endpoint_auth_method = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    tokens = relationship("OAuth2Token", back_populates="client")
    user_roles = relationship("UserRole", back_populates="client")

class OAuth2Token(Base):
    __tablename__ = "oauth2_tokens"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    token = Column(String, unique=True, index=True, nullable=False)
    token_type = Column(SQLEnum(TokenType), nullable=False)
    client_id = Column(String, ForeignKey("oauth2_clients.client_id"), nullable=False)
    user_id = Column(UUID, ForeignKey("user_credentials.id"), nullable=False)
    scope = Column(String)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    revoked_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    client = relationship("OAuth2Client", back_populates="tokens")
    user = relationship("UserCredential", back_populates="tokens")