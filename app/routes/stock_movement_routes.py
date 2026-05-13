from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.stock_movement_schema import StockMovementCreate, StockMovementUpdate, StockMovementResponse
from app.controllers.stock_movement_controller import (
    create_stock_movement,
    get_item_movements,
    get_user_movements,
    get_all_movements,
    get_movements_by_type,
    get_stock_movement,
    update_stock_movement,
    delete_stock_movement
)


router = APIRouter(prefix="/stock-movement", tags=["Stock Movements"])


# CREATE STOCK MOVEMENT
@router.post("/", response_model=StockMovementResponse)
def route_create_stock_movement(payload: StockMovementCreate, db: Session = Depends(get_db)):
    return create_stock_movement(payload, db)


# GET ALL MOVEMENTS
@router.get("/", response_model=list[StockMovementResponse])
def route_get_all_movements(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return get_all_movements(db, skip=skip, limit=limit)


# GET MOVEMENTS FOR AN ITEM
@router.get("/item/{item_id}", response_model=list[StockMovementResponse])
def route_get_item_movements(
    item_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return get_item_movements(item_id, db, skip=skip, limit=limit)


# GET MOVEMENTS BY USER
@router.get("/user/{user_id}", response_model=list[StockMovementResponse])
def route_get_user_movements(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return get_user_movements(user_id, db, skip=skip, limit=limit)


# GET MOVEMENTS BY TYPE
@router.get("/type/{movement_type}", response_model=list[StockMovementResponse])
def route_get_movements_by_type(
    movement_type: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return get_movements_by_type(movement_type, db, skip=skip, limit=limit)


# GET ONE MOVEMENT
@router.get("/{movement_id}", response_model=StockMovementResponse)
def route_get_stock_movement(movement_id: int, db: Session = Depends(get_db)):
    return get_stock_movement(movement_id, db)


# UPDATE MOVEMENT
@router.put("/{movement_id}", response_model=StockMovementResponse)
def route_update_stock_movement(
    movement_id: int,
    payload: StockMovementUpdate,
    db: Session = Depends(get_db)
):
    return update_stock_movement(movement_id, payload, db)


# DELETE MOVEMENT
@router.delete("/{movement_id}")
def route_delete_stock_movement(movement_id: int, db: Session = Depends(get_db)):
    return delete_stock_movement(movement_id, db)
