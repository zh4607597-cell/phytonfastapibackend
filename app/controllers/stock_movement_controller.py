from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.stock_movement_model import StockMovement
from app.models.inventory_model import InventoryItem
from app.schemas.stock_movement_schema import StockMovementCreate, StockMovementUpdate


ALLOWED_MOVEMENT_TYPES = {"in", "out", "transfer", "adjustment"}


# CREATE STOCK MOVEMENT
def create_stock_movement(data: StockMovementCreate, db: Session):
    # Validate item exists
    item = db.query(InventoryItem).filter(InventoryItem.id == data.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    movement_type = data.type.lower().strip()
    if movement_type not in ALLOWED_MOVEMENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid stock movement type '{data.type}'. Allowed values: {sorted(ALLOWED_MOVEMENT_TYPES)}"
        )

    # Create movement record
    movement = StockMovement(**data.dict())
    db.add(movement)

    # Update inventory quantity based on movement type
    if movement_type == "in":
        item.quantity += data.quantity
    elif movement_type == "out":
        if item.quantity < data.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        item.quantity -= data.quantity
    elif movement_type == "adjustment":
        item.quantity = data.quantity  # Set absolute quantity
    # For transfer, quantity doesn't change (just location tracking)

    try:
        db.commit()
        db.refresh(movement)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))

    return movement


# GET ALL MOVEMENTS FOR AN ITEM
def get_item_movements(item_id: int, db: Session, skip: int = 0, limit: int = 100):
    return db.query(StockMovement).filter(
        StockMovement.item_id == item_id
    ).order_by(StockMovement.timestamp.desc()).offset(skip).limit(limit).all()


# GET ALL MOVEMENTS BY USER
def get_user_movements(user_id: int, db: Session, skip: int = 0, limit: int = 100):
    return db.query(StockMovement).filter(
        StockMovement.user == user_id
    ).order_by(StockMovement.timestamp.desc()).offset(skip).limit(limit).all()


# GET ALL MOVEMENTS
def get_all_movements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(StockMovement).order_by(
        StockMovement.timestamp.desc()
    ).offset(skip).limit(limit).all()


# GET MOVEMENTS BY TYPE
def get_movements_by_type(movement_type: str, db: Session, skip: int = 0, limit: int = 100):
    return db.query(StockMovement).filter(
        StockMovement.type == movement_type
    ).order_by(StockMovement.timestamp.desc()).offset(skip).limit(limit).all()


# GET ONE MOVEMENT
def get_stock_movement(movement_id: int, db: Session):
    movement = db.query(StockMovement).filter(StockMovement.id == movement_id).first()
    if not movement:
        raise HTTPException(status_code=404, detail="Stock movement not found")
    return movement


# UPDATE MOVEMENT (Limited - usually movements are immutable)
def update_stock_movement(movement_id: int, data: StockMovementUpdate, db: Session):
    movement = get_stock_movement(movement_id, db)
    
    # Only allow updating certain fields
    allowed_fields = ['reason', 'from_type', 'to_type']
    for key, value in data.dict(exclude_unset=True).items():
        if key in allowed_fields:
            setattr(movement, key, value)
    
    db.commit()
    db.refresh(movement)
    return movement


# DELETE MOVEMENT (Should be rare - usually for corrections)
def delete_stock_movement(movement_id: int, db: Session):
    movement = get_stock_movement(movement_id, db)
    
    # Reverse the inventory change
    item = db.query(InventoryItem).filter(InventoryItem.id == movement.item_id).first()
    if item:
        if movement.type.lower() == "in":
            item.quantity -= movement.quantity
        elif movement.type.lower() == "out":
            item.quantity += movement.quantity
        elif movement.type.lower() == "adjustment":
            # Can't easily reverse adjustment without previous value
            pass
    
    db.delete(movement)
    db.commit()
    return {"detail": "Stock movement deleted and inventory adjusted"}
