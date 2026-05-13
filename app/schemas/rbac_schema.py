from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# --- PERMISSION ---
class PermissionBase(BaseModel):
    can_view: bool = False
    can_create: bool = False
    can_update: bool = False
    can_delete: bool = False

class PermissionCreate(PermissionBase):
    role_id: int
    feature_id: int

class PermissionUpdate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    role_id: int
    feature_id: int
    created_at: Optional[datetime] = None

# --- USER PERMISSION ---
class UserPermissionCreate(PermissionBase):
    user_id: int
    feature_id: int

class UserPermissionUpdate(PermissionBase):
    pass

class UserPermissionResponse(PermissionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    feature_id: int
    created_at: Optional[datetime] = None
    feature: Optional["FeatureResponse"] = None

# --- FEATURE ---
class FeatureBase(BaseModel):
    feature_name: str
    feature_key: str
    icon: Optional[str] = None
    path: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: int = 0
    is_active: bool = True
    description: Optional[str] = None

class FeatureCreate(FeatureBase):
    pass

class FeatureUpdate(FeatureBase):
    feature_name: Optional[str] = None
    feature_key: Optional[str] = None
    icon: Optional[str] = None
    path: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None

class FeatureResponse(FeatureBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# --- ROLE ---
class RoleBase(BaseModel):
    role_name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    role_name: Optional[str] = None
    description: Optional[str] = None

class RoleResponse(RoleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: Optional[datetime] = None

class PermissionCheck(BaseModel):
    feature_key: str
    action: str   # view, create, update, delete