from fastapi import HTTPException
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)
from app.models.customer_model import Customer
from app.models.city_model import City
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate


# GENERATE CUSTOMER CODE
def generate_customer_code(city: str, db: Session) -> str:
    """
    Gets customer code based on city code from cityies table.
    Format: ABC (city code only)
    Example: Rawalpindi → RWP
             Islamabad → ISB
    """
    if not city:
        return "N/A"
    
    # Look up city in cities table
    city_record = db.query(City).filter(City.city.ilike(city)).first()
    if not city_record:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found in cities reference. Please add it first.")
    
    # Return city code as customer code
    customer_code = city_record.city_code.upper()
    
    return customer_code


# CREATE
def create_customer(data: CustomerCreate, db: Session):
    # Generate customer code from city if available
    customer_code = "N/A"
    if data.city:
        customer_code = generate_customer_code(data.city, db)
    
    customer_data = data.dict()
    customer_data["customer_code"] = customer_code
    
    customer = Customer(**customer_data)
    db.add(customer)
    db.commit()
    db.refresh(customer)


    return customer

# GET ALL
def get_all_customers(db: Session):
    return db.query(Customer).all()

# GET ONE
def get_customer(customer_id: int, db: Session):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# GET BY CUSTOMER CODE
def get_customer_by_code(customer_code: str, db: Session):
    customer = db.query(Customer).filter(Customer.customer_code == customer_code).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# GET CUSTOMERS BY CITY
def get_customers_by_city(city: str, db: Session):
    return db.query(Customer).filter(Customer.city.ilike(city)).all()

# UPDATE
def update_customer(customer_id: int, data: CustomerUpdate, db: Session):
    customer = get_customer(customer_id, db)
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)


    return customer

# DELETE
def delete_customer(customer_id: int, db: Session):
    customer = get_customer(customer_id, db)
    db.delete(customer)
    db.commit()
    return {"detail": "Customer deleted successfully"}