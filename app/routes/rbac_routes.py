from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.rbac_schema import (
    RoleCreate, RoleUpdate, RoleResponse,
    FeatureCreate, FeatureUpdate, FeatureResponse,
    PermissionCreate, PermissionUpdate, PermissionResponse,
    UserPermissionCreate, UserPermissionUpdate, UserPermissionResponse
)
from app.controllers.rbac_controller import (
    create_role, get_roles, update_role, delete_role,
    create_feature, get_features, update_feature, delete_feature,
    create_permission, get_permissions, update_permission, delete_permission,
    create_user_permission, get_user_permissions, get_user_permissions_by_user, update_user_permission, delete_user_permission
)
from typing import List

router = APIRouter(prefix="/rbac", tags=["RBAC Management"])

# --- ROLES ---
@router.post("/roles", response_model=RoleResponse)
def route_create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role(role, db)

@router.get("/roles", response_model=List[RoleResponse])
def route_get_roles(db: Session = Depends(get_db)):
    return get_roles(db)

@router.put("/roles/{role_id}", response_model=RoleResponse)
def route_update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    return update_role(role_id, role, db)

@router.delete("/roles/{role_id}")
def route_delete_role(role_id: int, db: Session = Depends(get_db)):
    return delete_role(role_id, db)

# --- FEATURES ---
@router.post("/features", response_model=FeatureResponse)
def route_create_feature(feature: FeatureCreate, db: Session = Depends(get_db)):
    return create_feature(feature, db)

@router.get("/features", response_model=List[FeatureResponse])
def route_get_features(db: Session = Depends(get_db)):
    return get_features(db)

@router.put("/features/{feature_id}", response_model=FeatureResponse)
def route_update_feature(feature_id: int, feature: FeatureUpdate, db: Session = Depends(get_db)):
    return update_feature(feature_id, feature, db)

@router.delete("/features/{feature_id}")
def route_delete_feature(feature_id: int, db: Session = Depends(get_db)):
    return delete_feature(feature_id, db)

# --- ROLE PERMISSIONS ---
@router.post("/permissions", response_model=PermissionResponse)
def route_create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    return create_permission(permission, db)

@router.get("/permissions", response_model=List[PermissionResponse])
def route_get_permissions(db: Session = Depends(get_db)):
    return get_permissions(db)

@router.put("/permissions/{permission_id}", response_model=PermissionResponse)
def route_update_permission(permission_id: int, permission: PermissionUpdate, db: Session = Depends(get_db)):
    return update_permission(permission_id, permission, db)

@router.delete("/permissions/{permission_id}")
def route_delete_permission(permission_id: int, db: Session = Depends(get_db)):
    return delete_permission(permission_id, db)

# --- USER PERMISSIONS ---
@router.post("/user-permissions", response_model=UserPermissionResponse)
def route_create_user_permission(permission: UserPermissionCreate, db: Session = Depends(get_db)):
    return create_user_permission(permission, db)

@router.get("/user-permissions", response_model=List[UserPermissionResponse])
def route_get_user_permissions(db: Session = Depends(get_db)):
    return get_user_permissions(db)

@router.get("/user-permissions/user/{user_id}", response_model=List[UserPermissionResponse])
def route_get_user_permissions_by_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_permissions_by_user(user_id, db)

@router.put("/user-permissions/{permission_id}", response_model=UserPermissionResponse)
def route_update_user_permission(permission_id: int, permission: UserPermissionUpdate, db: Session = Depends(get_db)):
    return update_user_permission(permission_id, permission, db)

@router.delete("/user-permissions/{permission_id}")
def route_delete_user_permission(permission_id: int, db: Session = Depends(get_db)):
    return delete_user_permission(permission_id, db)
