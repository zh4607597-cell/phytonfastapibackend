from pydantic import BaseModel
from datetime import datetime

class AttachmentBase(BaseModel):
    file_name: str
    file_type: str | None = None

class AttachmentSchema(AttachmentBase):
    id: int
    lead_id: int
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True
