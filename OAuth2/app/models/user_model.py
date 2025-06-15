from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Sequence, UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

import enum
from datetime import datetime, UTC
from uuid import uuid4
class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOCKED = "locked"

class UserCredential(Base):
    __tablename__ = "user_credentials"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    hash_type = Column(String, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)

    details = relationship("UserDetail", back_populates="user", uselist=False)
    roles = relationship("UserRole", back_populates="user")
    tokens = relationship("OAuth2Token", back_populates="user")

class UserDetail(Base):
    __tablename__ = "user_details"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("user_credentials.id"), nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)

    user = relationship("UserCredential", back_populates="details")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, Sequence('roles_id_seq'), primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)

    users = relationship("UserRole", back_populates="role")
    role_permissions = relationship("RolePermission", back_populates="role")

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    role_permissions = relationship("RolePermission", back_populates="permission")

class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, Sequence('user_roles_id_seq'), primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("user_credentials.id"), nullable=False)
    client_id = Column(String, ForeignKey("oauth2_clients.client_id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)

    role = relationship("Role", back_populates="users")
    user = relationship("UserCredential", back_populates="roles")
    client = relationship("OAuth2Client", back_populates="user_roles")

class RolePermission(Base):
    __tablename__ = "role_permissions"
    id = Column(Integer, primary_key=True,autoincrement=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    permission_id = Column(Integer, ForeignKey('permissions.id'))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")
