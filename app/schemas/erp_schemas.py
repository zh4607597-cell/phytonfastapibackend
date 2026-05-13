from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: str
    category: Optional[str] = None
    unit_price: Decimal = 0.0
    recurring_price: Decimal = 0.0
    status: Optional[str] = "Active"
    type: Optional[str] = "Product"


class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    sku: Optional[str] = None
    unit_price: Optional[Decimal] = None

class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if v is None or v == "" or str(v).startswith("0000-00-00"):
            return None
        return v

    class Config:
        from_attributes = True

# Lead Product Schemas
class LeadProductBase(BaseModel):
    lead_id: int
    product_id: Optional[int] = None
    product_name: str
    description: Optional[str] = None
    quantity: int = 1
    unit_price: float = 0.0
    billing_cycle: Optional[str] = "One-time"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    tax: float = 0.0
    discount: float = 0.0
    total: float = 0.0

class LeadProductCreate(LeadProductBase):
    pass

class LeadProductUpdate(BaseModel):
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    billing_cycle: Optional[str] = None
    tax: Optional[float] = None
    discount: Optional[float] = None
    total: Optional[float] = None

class LeadProductResponse(LeadProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Invoice Item Schemas
class InvoiceItemBase(BaseModel):
    invoice_id: int
    product_id: Optional[int] = None
    item_name: str
    description: Optional[str] = None
    quantity: int = 1
    unit_price: float = 0.0
    tax_amount: float = 0.0
    discount_amount: float = 0.0
    total: float = 0.0

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItemResponse(InvoiceItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Payment Schemas
class PaymentBase(BaseModel):
    invoice_id: int
    amount: float
    payment_date: Optional[datetime] = None
    payment_method: str
    transaction_id: Optional[str] = None
    status: Optional[str] = "Completed"
    notes: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Contract Template Schemas
class ContractTemplateBase(BaseModel):
    name: str
    file_path: str
    content: Optional[str] = None
    is_active: Optional[bool] = True

class ContractTemplateCreate(ContractTemplateBase):
    pass

class ContractTemplateResponse(ContractTemplateBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Contract Schemas
class ContractBase(BaseModel):
    lead_id: int
    template_id: int
    contract_number: str
    file_path: Optional[str] = None
    signed_file_path: Optional[str] = None
    status: Optional[str] = "Draft"
    version: Optional[int] = 1

class ContractCreate(ContractBase):
    pass

class ContractResponse(ContractBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Activity Schemas
class ActivityBase(BaseModel):
    lead_id: Optional[int] = None
    performed_by: Optional[str] = None
    action: str
    entity_type: str
    entity_id: int
    details: Optional[str] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityResponse(ActivityBase):
    id: int
    created_at: Optional[datetime] = None

    @field_validator('created_at', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if v is None or v == "" or str(v).startswith("0000-00-00"):
            return None
        return v

    class Config:
        from_attributes = True

# Attachment Schemas
class AttachmentBase(BaseModel):
    entity_type: str
    entity_id: int
    file_name: str
    file_path: str
    file_type: str
    file_size: int

class AttachmentCreate(AttachmentBase):
    pass

class AttachmentResponse(AttachmentBase):
    id: int
    created_at: Optional[datetime] = None

    @field_validator('created_at', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if v is None or v == "" or str(v).startswith("0000-00-00"):
            return None
        return v

    class Config:
        from_attributes = True
