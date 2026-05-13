from fastapi import APIRouter, Depends
from dependencies.permission import permission_required

router = APIRouter(prefix="/inventory-v2", tags=["Inventory V2"])

# CREATE
@router.post("/")
def create_inventory_v2(
    _=Depends(permission_required("inventory", "create"))
):
    return {"msg": "Inventory V2 created"}

# READ
@router.get("/")
def get_inventory_v2(
    _=Depends(permission_required("inventory", "read"))
):
    return {"msg": "Inventory V2 list"}

# UPDATE
@router.put("/{id}")
def update_inventory_v2(
    id: int,
    _=Depends(permission_required("inventory", "update"))
):
    return {"msg": f"Inventory V2 {id} updated"}

# DELETE
@router.delete("/{id}")
def delete_inventory_v2(
    id: int,
    _=Depends(permission_required("inventory", "delete"))
):
    return {"msg": f"Inventory V2 {id} deleted"}