from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Response
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.attachment import Attachment
from app.models.activity import Activity
from app.schemas.attachment import AttachmentSchema
import os
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

STORAGE_PATH = "public/storage/attachments"

@router.get("/{lead_id}", response_model=List[AttachmentSchema])
def list_attachments(lead_id: int, db: Session = Depends(get_db)):
    return db.query(Attachment).filter(Attachment.lead_id == lead_id).all()

@router.post("/{lead_id}")
async def upload_attachment(lead_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    os.makedirs(STORAGE_PATH, exist_ok=True)
    fpath = f"{STORAGE_PATH}/L{lead_id}_{file.filename}"
    
    with open(fpath, "wb") as f:
        f.write(await file.read())
    
    attachment = Attachment(
        lead_id=lead_id,
        file_name=file.filename,
        file_path=fpath,
        file_type=file.content_type
    )
    db.add(attachment)
    db.add(Activity(lead_id=lead_id, action="File Uploaded", detail=f"Uploaded {file.filename}"))
    db.commit()
    return {"message": "File uploaded", "filename": file.filename}

@router.get("/download/{id}")
def download_attachment(id: int, db: Session = Depends(get_db)):
    att = db.query(Attachment).filter(Attachment.id == id).first()
    if not att or not os.path.exists(att.file_path): raise HTTPException(404, "File not found")
    
    with open(att.file_path, "rb") as f:
        content = f.read()
    return Response(content=content, media_type=att.file_type or "application/octet-stream", headers={"Content-Disposition": f"attachment; filename={att.file_name}"})

@router.delete("/{id}")
def delete_attachment(id: int, db: Session = Depends(get_db)):
    att = db.query(Attachment).filter(Attachment.id == id).first()
    if not att: raise HTTPException(404)
    
    if os.path.exists(att.file_path):
        os.remove(att.file_path)
    
    db.delete(att)
    db.commit()
    return {"message": "Deleted"}
