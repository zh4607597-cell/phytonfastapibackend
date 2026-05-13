from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate, CustomerResponse
from app.controllers.customer_controller import (
    create_customer, get_all_customers,
    get_customer, get_customer_by_code, get_customers_by_city,
    update_customer, delete_customer
)


router = APIRouter(prefix="/customer", tags=["Customers"])



@router.post("/", response_model=CustomerResponse)
def route_create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(payload, db)

@router.get("/", response_model=list[CustomerResponse])
def route_get_all_customers(db: Session = Depends(get_db)):
    return get_all_customers(db)

@router.get("/code/{customer_code}", response_model=CustomerResponse)
def route_get_customer_by_code(customer_code: str, db: Session = Depends(get_db)):
    return get_customer_by_code(customer_code, db)

@router.get("/city/{city}", response_model=list[CustomerResponse])
def route_get_customers_by_city(city: str, db: Session = Depends(get_db)):
    return get_customers_by_city(city, db)

@router.get("/{customer_id}", response_model=CustomerResponse)
def route_get_customer(customer_id: int, db: Session = Depends(get_db)):
    return get_customer(customer_id, db)

@router.put("/{customer_id}", response_model=CustomerResponse)
def route_update_customer(customer_id: int, payload: CustomerUpdate, db: Session = Depends(get_db)):
    return update_customer(customer_id, payload, db)

@router.delete("/{customer_id}")
def route_delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return delete_customer(customer_id, db)