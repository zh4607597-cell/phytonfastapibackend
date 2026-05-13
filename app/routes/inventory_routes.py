from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.inventory_schema import InventoryItemCreate, InventoryItemUpdate, InventoryItemResponse
from app.controllers.inventory_controller import (
    create_inventory_item,
    get_all_inventory_items,
    get_inventory_item,
    get_inventory_item_by_sku,
    update_inventory_item,
    delete_inventory_item,
    check_stock_level,
    update_inventory_quantity
)


router = APIRouter(prefix="/inventory", tags=["Inventory"])


# CREATE
@router.post("/", response_model=InventoryItemResponse)
def route_create_inventory_item(payload: InventoryItemCreate, db: Session = Depends(get_db)):
    return create_inventory_item(payload, db)


# GET ALL
@router.get("/", response_model=list[InventoryItemResponse])
def route_get_all_inventory_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return get_all_inventory_items(db, skip=skip, limit=limit)


# GET ONE
@router.get("/{item_id}", response_model=InventoryItemResponse)
def route_get_inventory_item(item_id: int, db: Session = Depends(get_db)):
    return get_inventory_item(item_id, db)


# GET BY SKU
@router.get("/sku/{sku}", response_model=InventoryItemResponse)
def route_get_inventory_item_by_sku(sku: str, db: Session = Depends(get_db)):
    return get_inventory_item_by_sku(sku, db)


# UPDATE
@router.put("/{item_id}", response_model=InventoryItemResponse)
def route_update_inventory_item(
    item_id: int,
    payload: InventoryItemUpdate,
    db: Session = Depends(get_db)
):
    return update_inventory_item(item_id, payload, db)


# DELETE
@router.delete("/{item_id}")
def route_delete_inventory_item(item_id: int, db: Session = Depends(get_db)):
    return delete_inventory_item(item_id, db)


# CHECK STOCK LEVEL
@router.get("/{item_id}/stock-level")
def route_check_stock_level(item_id: int, db: Session = Depends(get_db)):
    return check_stock_level(item_id, db)


# UPDATE QUANTITY
@router.patch("/{item_id}/quantity")
def route_update_quantity(
    item_id: int,
    quantity_change: int = Query(..., description="Amount to add/subtract from quantity"),
    db: Session = Depends(get_db)
):
    return update_inventory_quantity(item_id, quantity_change, db)
