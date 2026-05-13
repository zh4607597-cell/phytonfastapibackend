from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.city_model import City
from app.schemas.city_schema import CityCreate, CityUpdate


# CREATE
def create_city(data: CityCreate, db: Session):
    # Check if city already exists
    existing_city = db.query(City).filter(City.city.ilike(data.city)).first()
    if existing_city:
        raise HTTPException(status_code=400, detail="City already exists")

    # Check if city code already exists
    existing_code = db.query(City).filter(City.city_code.ilike(data.city_code)).first()
    if existing_code:
        raise HTTPException(status_code=400, detail="City code already exists")

    city = City(**data.dict())
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


# GET ALL
def get_all_cities(db: Session):
    return db.query(City).order_by(City.city.asc()).all()


# GET ONE BY ID
def get_city(city_id: int, db: Session):
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


# GET BY CITY NAME
def get_city_by_name(city_name: str, db: Session):
    city = db.query(City).filter(City.city.ilike(city_name)).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


# GET BY CITY CODE
def get_city_by_code(city_code: str, db: Session):
    city = db.query(City).filter(City.city_code.ilike(city_code)).first()
    if not city:
        raise HTTPException(status_code=404, detail="City code not found")
    return city


# UPDATE
def update_city(city_id: int, data: CityUpdate, db: Session):
    city = get_city(city_id, db)

    # Check if new city name exists
    if data.city and data.city != city.city:
        existing = db.query(City).filter(City.city.ilike(data.city)).first()
        if existing:
            raise HTTPException(status_code=400, detail="City name already exists")

    # Check if new city code exists
    if data.city_code and data.city_code != city.city_code:
        existing = db.query(City).filter(City.city_code.ilike(data.city_code)).first()
        if existing:
            raise HTTPException(status_code=400, detail="City code already exists")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(city, key, value)

    db.commit()
    db.refresh(city)
    return city


# DELETE
def delete_city(city_id: int, db: Session):
    city = get_city(city_id, db)
    db.delete(city)
    db.commit()
    return {"detail": "City deleted successfully"}


# SEARCH
def search_cities(query: str, db: Session):
    return db.query(City).filter(
        (City.city.ilike(f"%{query}%")) | (City.city_code.ilike(f"%{query}%"))
    ).order_by(City.city.asc()).all()
