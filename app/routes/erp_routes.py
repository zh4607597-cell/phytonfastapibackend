from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from app.deps import get_db, PermissionChecker
from app.services.erp_service import ERPService

from app.schemas.erp_schemas import (
    ProductCreate, ProductUpdate, ProductResponse,
    LeadProductCreate, LeadProductResponse,
    PaymentCreate, PaymentResponse,
    ActivityResponse, ContractTemplateResponse,
    ContractResponse
)
from app.models.erp_models import (
    Product, LeadProduct, InvoiceItem, Payment,
    ContractTemplate, Contract, Activity, Attachment
)
from app.models.invoice_model import Invoice
from typing import List, Optional
import os, shutil

router = APIRouter()

# ─────────────── PRODUCT ROUTES ───────────────
@router.get("/products", response_model=List[ProductResponse], dependencies=[Depends(PermissionChecker("leads_crm", "can_view"))])
def get_products(db: Session = Depends(get_db)):
    return ERPService.get_products(db)

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p

@router.post("/products", response_model=ProductResponse, dependencies=[Depends(PermissionChecker("leads_crm", "can_create"))])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return ERPService.create_product(db, product)

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    updated = ERPService.update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(p)
    db.commit()
    return {"message": "Product deleted"}

# ─────────────── LEAD PRODUCT ROUTES ───────────────
@router.get("/lead/{lead_id}/products", response_model=List[LeadProductResponse], dependencies=[Depends(PermissionChecker("leads_crm", "can_view"))])
def get_lead_products(lead_id: int, db: Session = Depends(get_db)):
    return ERPService.get_lead_products(db, lead_id)

@router.post("/lead/{lead_id}/products", response_model=LeadProductResponse)
def add_product_to_lead(lead_id: int, lead_product: LeadProductCreate, db: Session = Depends(get_db)):
    lp = lead_product.model_dump()
    lp["lead_id"] = lead_id
    from app.schemas.erp_schemas import LeadProductCreate as LPC
    return ERPService.add_product_to_lead(db, LPC(**lp))

@router.put("/lead/{lead_id}/products", dependencies=[Depends(PermissionChecker("leads_crm", "can_update"))])
def save_lead_products(lead_id: int, products: List[dict], db: Session = Depends(get_db)):
    return ERPService.save_lead_products(db, lead_id, products)

@router.delete("/lead/{lead_id}/products/{lp_id}")
def remove_lead_product(lead_id: int, lp_id: int, db: Session = Depends(get_db)):
    lp = db.query(LeadProduct).filter(LeadProduct.id == lp_id, LeadProduct.lead_id == lead_id).first()
    if not lp:
        raise HTTPException(status_code=404, detail="Lead product not found")
    db.delete(lp)
    db.commit()
    return {"message": "Product removed"}


# ─────────────── INVOICE ROUTES ───────────────
@router.get("/invoices")
def get_all_invoices(lead_id: Optional[int] = None, db: Session = Depends(get_db)):
    return ERPService.get_invoices(db, lead_id)

@router.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    inv = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv

@router.post("/invoices/generate/{lead_id}", dependencies=[Depends(PermissionChecker("leads_crm", "can_update"))])
def generate_invoice(lead_id: int, billing_type: str = "One-time", db: Session = Depends(get_db)):
    invoice = ERPService.generate_invoice(db, lead_id, billing_type)
    if not invoice:
        raise HTTPException(status_code=400, detail="Could not generate invoice. Ensure lead has products.")
    return invoice

@router.patch("/invoices/{invoice_id}/status")
def update_invoice_status(invoice_id: int, payload: dict, db: Session = Depends(get_db)):
    inv = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    inv.status = payload.get("status", inv.status)
    db.commit()
    db.refresh(inv)
    return inv

@router.get("/invoices/{invoice_id}/pdf")
def download_invoice_pdf(invoice_id: int, db: Session = Depends(get_db)):
    pdf_path = ERPService.generate_invoice_pdf(db, invoice_id)
    if not pdf_path or not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF could not be generated")
    return FileResponse(pdf_path, media_type="application/pdf", filename=os.path.basename(pdf_path))

# ─────────────── PAYMENT ROUTES ───────────────
@router.get("/payments", response_model=List[PaymentResponse])
def get_payments(invoice_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(Payment)
    if invoice_id:
        q = q.filter(Payment.invoice_id == invoice_id)
    return q.order_by(Payment.created_at.desc()).all()

@router.post("/payments", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    return ERPService.create_payment(db, payment)

# ─────────────── CONTRACT TEMPLATE ROUTES ───────────────
@router.get("/contracts/templates", response_model=List[ContractTemplateResponse])
def get_templates(db: Session = Depends(get_db)):
    return db.query(ContractTemplate).filter(ContractTemplate.is_active == True).all()

@router.post("/contracts/templates")
async def upload_template(name: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    os.makedirs("storage/templates", exist_ok=True)
    safe_name = file.filename.replace(" ", "_")
    file_path = f"storage/templates/{safe_name}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    tmpl = ContractTemplate(name=name, file_path=file_path, is_active=True)
    db.add(tmpl)
    db.commit()
    db.refresh(tmpl)
    return tmpl

@router.get("/contracts/templates/{template_id}/download")
def download_template(template_id: int, db: Session = Depends(get_db)):
    tmpl = db.query(ContractTemplate).filter(ContractTemplate.id == template_id).first()
    if not tmpl or not os.path.exists(tmpl.file_path):
        raise HTTPException(status_code=404, detail="Template not found")
    return FileResponse(tmpl.file_path, filename=os.path.basename(tmpl.file_path))

# ─────────────── CONTRACT ROUTES ───────────────
@router.get("/contracts")
def get_contracts(lead_id: Optional[int] = None, db: Session = Depends(get_db)):
    return ERPService.get_contracts(db, lead_id)

@router.post("/contracts/generate/{lead_id}", dependencies=[Depends(PermissionChecker("leads_crm", "can_update"))])
def generate_contract(lead_id: int, template_id: int, db: Session = Depends(get_db)):
    contract = ERPService.generate_contract(db, lead_id, template_id)
    if not contract:
        raise HTTPException(status_code=400, detail="Could not generate contract. Check lead and template.")
    return contract

@router.get("/contracts/{contract_id}", response_model=dict)
def get_contract(contract_id: int, db: Session = Depends(get_db)):
    c = ERPService.get_contract(db, contract_id)
    if not c:
        raise HTTPException(status_code=404, detail="Contract not found")
    return c

@router.put("/contracts/{contract_id}", response_model=dict)
def update_contract(contract_id: int, data: dict, db: Session = Depends(get_db)):
    c = ERPService.update_contract(db, contract_id, data)
    if not c:
        raise HTTPException(status_code=404, detail="Contract not found")
    return c

@router.delete("/contracts/{contract_id}")
def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    success = ERPService.delete_contract(db, contract_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contract not found")
    return {"detail": "Contract deleted"}

@router.get("/contracts/{contract_id}/download")
def download_contract(contract_id: int, type: str = "docx", db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    file_path = contract.file_path
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Contract file not found on disk")
    media = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    return FileResponse(file_path, media_type=media, filename=os.path.basename(file_path))

@router.post("/contracts/{contract_id}/upload-signed")
async def upload_signed_contract(contract_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    os.makedirs("storage/signed_contracts", exist_ok=True)
    safe_name = file.filename.replace(" ", "_")
    file_path = f"storage/signed_contracts/{contract_id}_{safe_name}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    contract.signed_file_path = file_path
    contract.status = "Signed"
    db.commit()
    db.refresh(contract)
    return {"message": "Signed contract uploaded", "status": "Signed"}

# ─────────────── ACTIVITY ROUTES ───────────────
@router.get("/activities", response_model=List[ActivityResponse])
def get_activities(lead_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(Activity)
    if lead_id:
        q = q.filter(Activity.lead_id == lead_id)
    return q.order_by(Activity.created_at.desc()).limit(100).all()

@router.get("/lead/{lead_id}/activity", response_model=List[ActivityResponse])
def get_lead_activity(lead_id: int, db: Session = Depends(get_db)):
    return ERPService.get_lead_activity_timeline(db, lead_id)

# ─────────────── ATTACHMENT ROUTES ───────────────
@router.post("/attachments/upload")
async def upload_attachment(
    entity_type: str = Form(...),
    entity_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    os.makedirs(f"storage/attachments/{entity_type}", exist_ok=True)
    safe_name = file.filename.replace(" ", "_")
    file_path = f"storage/attachments/{entity_type}/{entity_id}_{safe_name}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    att = Attachment(
        entity_type=entity_type,
        entity_id=entity_id,
        file_name=file.filename,
        file_path=file_path,
        file_type=file.content_type or "application/octet-stream",
        file_size=os.path.getsize(file_path)
    )
    db.add(att)
    db.commit()
    db.refresh(att)
    return att

@router.get("/attachments")
def get_attachments(entity_type: str, entity_id: int, db: Session = Depends(get_db)):
    return db.query(Attachment).filter(
        Attachment.entity_type == entity_type,
        Attachment.entity_id == entity_id
    ).all()
