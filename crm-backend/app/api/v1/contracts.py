from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Response
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.contract import Contract
from app.models.contract_template import ContractTemplate
from app.models.lead import Lead
from app.services.contract_service import ContractService
import os
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

STORAGE_PATH = "public/storage"

@router.get("/")
def list_contracts(lead_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Contract)
    if lead_id: query = query.filter(Contract.lead_id == lead_id)
    contracts = query.all()
    res = []
    for c in contracts:
        lead = db.query(Lead).filter(Lead.id == c.lead_id).first()
        tmpl = db.query(ContractTemplate).filter(ContractTemplate.id == c.template_id).first()
        res.append({
            "id": c.id,
            "lead_id": c.lead_id,
            "lead_name": lead.lead_name if lead else "Unknown",
            "template_name": tmpl.name if tmpl else "Template",
            "version": c.version,
            "status": c.status,
            "created_at": c.created_at,
            "generated_docx_path": c.generated_docx_path
        })
    return res

@router.get("/templates")
def list_templates(db: Session = Depends(get_db)):
    return db.query(ContractTemplate).all()

@router.post("/templates")
async def upload_template(name: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    os.makedirs(f"{STORAGE_PATH}/templates", exist_ok=True)
    fpath = f"{STORAGE_PATH}/templates/{file.filename}"
    with open(fpath, "wb") as f: f.write(await file.read())
    tmpl = ContractTemplate(name=name, file_path=fpath)
    db.add(tmpl)
    db.commit()
    return {"message": "Template uploaded"}

@router.post("/generate/{lead_id}")
def generate_contract(lead_id: int, template_id: int, db: Session = Depends(get_db)):
    contract, error = ContractService.generate_contract(db, lead_id, template_id)
    if error: raise HTTPException(400, error)
    return {"message": "Contract generated", "id": contract.id}

@router.get("/{id}/download")
def download_contract(id: int, db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == id).first()
    if not contract or not contract.generated_docx_path: raise HTTPException(404)
    with open(contract.generated_docx_path, "rb") as f:
        content = f.read()
    return Response(content=content, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers={"Content-Disposition": f"attachment; filename=Contract_{id}.docx"})

@router.post("/{id}/upload-signed")
async def upload_signed(id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == id).first()
    if not contract: raise HTTPException(404)
    
    os.makedirs(f"{STORAGE_PATH}/signed", exist_ok=True)
    fpath = f"{STORAGE_PATH}/signed/SIGNED_{id}_{file.filename}"
    with open(fpath, "wb") as f: f.write(await file.read())
    
    contract.signed_doc_path = fpath
    contract.status = "Signed"
    lead = db.query(Lead).filter(Lead.id == contract.lead_id).first()
    if lead: lead.contract_status = "Signed"
    db.commit()
    return {"message": "Signed contract uploaded"}
