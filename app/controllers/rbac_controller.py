from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.rbac_models import Role, Feature, Permission, UserPermission
from app.schemas.rbac_schema import (
    RoleCreate, RoleUpdate, 
    FeatureCreate, FeatureUpdate, 
    PermissionCreate, PermissionUpdate,
    UserPermissionCreate, UserPermissionUpdate
)

# --- ROLE CONTROLLERS ---
def create_role(role: RoleCreate, db: Session):
    db_role = Role(role_name=role.role_name, description=role.description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_roles(db: Session):
    return db.query(Role).all()

def update_role(role_id: int, role: RoleUpdate, db: Session):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    for field, value in role.model_dump(exclude_unset=True).items():
        setattr(db_role, field, value)
    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(role_id: int, db: Session):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(db_role)
    db.commit()
    return {"detail": "Role deleted"}

# --- FEATURE CONTROLLERS ---
def create_feature(feature: FeatureCreate, db: Session):
    db_feature = Feature(
        feature_name=feature.feature_name, 
        feature_key=feature.feature_key, 
        icon=feature.icon,
        path=feature.path,
        parent_id=feature.parent_id,
        sort_order=feature.sort_order,
        is_active=feature.is_active,
        description=feature.description
    )
    db.add(db_feature)
    db.commit()
    db.refresh(db_feature)
    return db_feature

def get_features(db: Session):
    return db.query(Feature).all()

def update_feature(feature_id: int, feature: FeatureUpdate, db: Session):
    db_feature = db.query(Feature).filter(Feature.id == feature_id).first()
    if not db_feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    for field, value in feature.model_dump(exclude_unset=True).items():
        setattr(db_feature, field, value)
    db.commit()
    db.refresh(db_feature)
    return db_feature

def delete_feature(feature_id: int, db: Session):
    db_feature = db.query(Feature).filter(Feature.id == feature_id).first()
    if not db_feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    db.delete(db_feature)
    db.commit()
    return {"detail": "Feature deleted"}

# --- PERMISSION CONTROLLERS ---
def create_permission(permission: PermissionCreate, db: Session):
    db_permission = Permission(
        role_id=permission.role_id,
        feature_id=permission.feature_id,
        can_view=permission.can_view,
        can_create=permission.can_create,
        can_update=permission.can_update,
        can_delete=permission.can_delete
    )
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def get_permissions(db: Session):
    return db.query(Permission).all()

def update_permission(permission_id: int, permission: PermissionUpdate, db: Session):
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    for field, value in permission.model_dump(exclude_unset=True).items():
        setattr(db_permission, field, value)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def delete_permission(permission_id: int, db: Session):
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.delete(db_permission)
    db.commit()
    return {"detail": "Permission deleted"}

# --- USER PERMISSION CONTROLLERS ---
def create_user_permission(permission: UserPermissionCreate, db: Session):
    db_permission = UserPermission(
        user_id=permission.user_id,
        feature_id=permission.feature_id,
        can_view=permission.can_view,
        can_create=permission.can_create,
        can_update=permission.can_update,
        can_delete=permission.can_delete
    )
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def get_user_permissions(db: Session):
    return db.query(UserPermission).all()

def get_user_permissions_by_user(user_id: int, db: Session):
    return db.query(UserPermission).filter(UserPermission.user_id == user_id).all()

def update_user_permission(permission_id: int, permission: UserPermissionUpdate, db: Session):
    db_permission = db.query(UserPermission).filter(UserPermission.id == permission_id).first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="User Permission not found")
    for field, value in permission.model_dump(exclude_unset=True).items():
        setattr(db_permission, field, value)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def delete_user_permission(permission_id: int, db: Session):
    db_permission = db.query(UserPermission).filter(UserPermission.id == permission_id).first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="User Permission not found")
    db.delete(db_permission)
    db.commit()
    return {"detail": "User Permission deleted"}
