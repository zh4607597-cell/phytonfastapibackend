from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.inventory_model import InventoryItem
from app.schemas.inventory_schema import InventoryItemCreate, InventoryItemUpdate


# CREATE
def create_inventory_item(data: InventoryItemCreate, db: Session):
    # Check if SKU already exists
    existing = db.query(InventoryItem).filter(InventoryItem.sku == data.sku).first()
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")
    
    item = InventoryItem(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# GET ALL
def get_all_inventory_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(InventoryItem).offset(skip).limit(limit).all()


# GET ONE
def get_inventory_item(item_id: int, db: Session):
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item


# GET BY SKU
def get_inventory_item_by_sku(sku: str, db: Session):
    item = db.query(InventoryItem).filter(InventoryItem.sku == sku).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item


# UPDATE
def update_inventory_item(item_id: int, data: InventoryItemUpdate, db: Session):
    item = get_inventory_item(item_id, db)
    
    # Check if updating SKU to a value that already exists
    if data.sku and data.sku != item.sku:
        existing = db.query(InventoryItem).filter(InventoryItem.sku == data.sku).first()
        if existing:
            raise HTTPException(status_code=400, detail="SKU already exists")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)
    
    db.commit()
    db.refresh(item)
    return item


# DELETE
def delete_inventory_item(item_id: int, db: Session):
    item = get_inventory_item(item_id, db)
    db.delete(item)
    db.commit()
    return {"detail": "Inventory item deleted successfully"}


# CHECK STOCK LEVEL
def check_stock_level(item_id: int, db: Session):
    item = get_inventory_item(item_id, db)
    return {
        "id": item.id,
        "name": item.name,
        "sku": item.sku,
        "quantity": item.quantity,
        "min_stock": item.min_stock,
        "max_stock": item.max_stock,
        "status": "low" if item.quantity < item.min_stock else "sufficient" if item.quantity <= item.max_stock else "excess"
    }


# UPDATE QUANTITY
def update_inventory_quantity(item_id: int, quantity_change: int, db: Session):
    item = get_inventory_item(item_id, db)
    item.quantity += quantity_change
    db.commit()
    db.refresh(item)
    return item
