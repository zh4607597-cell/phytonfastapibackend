from pydantic import BaseModel
from datetime import datetime

class ActivitySchema(BaseModel):
    id: int
    lead_id: int
    action: str
    detail: str | None = None
    performed_by: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
