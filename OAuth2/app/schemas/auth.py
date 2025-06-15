from pydantic import BaseModel, HttpUrl, field_validator
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class OAuth2ClientBase(BaseModel):
    name: str
    description: Optional[str] = None
    redirect_uris: List[str]
    grant_types: List[str]
    response_types: List[str]
    scope: str
    token_endpoint_auth_method: str

class OAuth2ClientCreate(OAuth2ClientBase):
    class Config:
        json_encoders = {
            HttpUrl: str
        }
        
class OAuth2ClientResponse(OAuth2ClientBase):
    id: UUID
    client_id: str
    client_secret: str
    created_at: datetime
    updated_at: datetime

    @field_validator('redirect_uris', 'grant_types', 'response_types', mode='before')
    @classmethod
    def split_string_to_list(cls, v):
        if isinstance(v, str):
            return [item.strip() for item in v.split(',')]
        return v

    class Config:
        from_attributes = True

class AuthorizationRequest(BaseModel):
    client_id: str
    response_type: str
    redirect_uri: str
    scope: str
    state: Optional[str] = None

class AuthorizationResponse(BaseModel):
    code: str
    state: Optional[str] = None