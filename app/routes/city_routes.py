from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.city_schema import CityCreate, CityUpdate, CityResponse
from app.controllers.city_controller import (
    create_city,
    get_all_cities,
    get_city,
    get_city_by_name,
    get_city_by_code,
    update_city,
    delete_city,
    search_cities
)


router = APIRouter(prefix="/cities", tags=["Cities"])


# CREATE
@router.post("/", response_model=CityResponse)
def route_create_city(payload: CityCreate, db: Session = Depends(get_db)):
    return create_city(payload, db)


# GET ALL
@router.get("/", response_model=list[CityResponse])
def route_get_all_cities(db: Session = Depends(get_db)):
    return get_all_cities(db)


# SEARCH CITIES
@router.get("/search", response_model=list[CityResponse])
def route_search_cities(
    q: str = Query(..., description="Search by city name or code"),
    db: Session = Depends(get_db)
):
    return search_cities(q, db)


# GET BY CITY NAME
@router.get("/name/{city_name}", response_model=CityResponse)
def route_get_city_by_name(city_name: str, db: Session = Depends(get_db)):
    return get_city_by_name(city_name, db)


# GET BY CITY CODE
@router.get("/code/{city_code}", response_model=CityResponse)
def route_get_city_by_code(city_code: str, db: Session = Depends(get_db)):
    return get_city_by_code(city_code, db)


# GET BY ID
@router.get("/{city_id}", response_model=CityResponse)
def route_get_city(city_id: int, db: Session = Depends(get_db)):
    return get_city(city_id, db)


# UPDATE
@router.put("/{city_id}", response_model=CityResponse)
def route_update_city(
    city_id: int,
    payload: CityUpdate,
    db: Session = Depends(get_db)
):
    return update_city(city_id, payload, db)


# DELETE
@router.delete("/{city_id}")
def route_delete_city(city_id: int, db: Session = Depends(get_db)):
    return delete_city(city_id, db)
