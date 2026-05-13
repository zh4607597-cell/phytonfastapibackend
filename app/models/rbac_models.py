from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    role_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True)
    feature_name = Column(String(100))
    feature_key = Column(String(100), unique=True)
    icon = Column(String(100), nullable=True)
    path = Column(String(255), nullable=True)
    parent_id = Column(Integer, ForeignKey("features.id"), nullable=True)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    feature_id = Column(Integer, ForeignKey("features.id"))

    can_view = Column(Boolean, default=False)
    can_create = Column(Boolean, default=False)
    can_update = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("role_id", "feature_id"),
    )

class UserPermission(Base):
    __tablename__ = "user_permissions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    feature_id = Column(Integer, ForeignKey("features.id"))

    can_view = Column(Boolean, default=False)
    can_create = Column(Boolean, default=False)
    can_update = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "feature_id"),
    )

    feature = relationship("Feature")