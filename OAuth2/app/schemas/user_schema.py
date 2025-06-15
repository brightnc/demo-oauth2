from uuid import UUID
from pydantic import BaseModel, ConfigDict

class UserDetail(BaseModel):
    name: str
    email: str

class UserRegister(BaseModel):
    username: str
    password: str
    details: UserDetail
    class Config:
        from_attributes = True

class UserRegisterResponse(BaseModel):
    id: str
    model_config = ConfigDict(from_attributes=True)