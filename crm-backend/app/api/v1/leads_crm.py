from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.db import SessionLocal
from app.models.lead import Lead
from app.models.product import Product
from app.models.lead_product import LeadProduct
from app.models.activity import Activity
from app.schemas.lead_crm import LeadProductSchema, LeadProductResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/{id}")
def get_lead_enhanced(id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == id).first()
    if not lead: raise HTTPException(404, "Lead not found")
    return lead

@router.get("/{id}/products", response_model=List[LeadProductResponse])
def get_lead_products(id: int, db: Session = Depends(get_db)):
    lps = db.query(LeadProduct).filter(LeadProduct.lead_id == id).all()
    res = []
    for lp in lps:
        prod = db.query(Product).filter(Product.id == lp.product_id).first()
        lp.product_name = prod.name if prod else "Unknown"
        lp.product_description = prod.description if prod else ""
        res.append(lp)
    return res

@router.put("/{id}/products")
def update_lead_products(id: int, products: List[LeadProductSchema], db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == id).first()
    if not lead: raise HTTPException(404, "Lead not found")
    
    db.query(LeadProduct).filter(LeadProduct.lead_id == id).delete()
    for p in products:
        if not p.product_id: continue
        new_lp = LeadProduct(lead_id=id, **p.dict())
        db.add(new_lp)
    
    db.add(Activity(lead_id=id, action="Products Updated", detail=f"Updated {len(products)} products"))
    db.commit()
    return {"message": "Products updated"}
