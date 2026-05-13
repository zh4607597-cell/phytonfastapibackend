from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Union
from app.schemas.lead_schemas import LeadCreate, LeadUpdate, LeadOut, LeadApproval, LeadStatusUpdate
from app.deps import get_db, PermissionChecker
from app.controllers.lead_controllers import (
    create_lead_controller,
    get_all_leads_controller,
    get_lead_by_id_controller,
    update_lead_controller,
    delete_lead_controller,
    approve_lead_controller,
    convert_lead_to_customer_erp,
    get_erp_leads_controller,
    get_erp_lead_by_name_controller,
    save_erp_lead_locally_controller,
    update_lead_status_controller
)

router = APIRouter(prefix="/lead", tags=["Leads"])

@router.get("/erp/leads", dependencies=[Depends(PermissionChecker("leads_crm", "can_view"))])
def route_get_erp_leads(status: str = "Feasibility-Send"):
    """
    Fetches leads from the ERP filtered by status.
    """
    return get_erp_leads_controller(status=status)

@router.get("/erp/leads/{name}", dependencies=[Depends(PermissionChecker("leads_crm", "can_view"))])
def route_get_erp_lead_by_name(name: str):
    """
    Fetches a single lead from ERP by name.
    """
    return get_erp_lead_by_name_controller(name)

@router.post("/erp/save", dependencies=[Depends(PermissionChecker("leads_crm", "can_update"))])
def route_save_erp_lead(data: dict, db: Session = Depends(get_db)):
    """
    Saves or updates an ERP lead in the local CRM.
    """
    return save_erp_lead_locally_controller(data, db)

@router.post("/convert-to-customer", dependencies=[Depends(PermissionChecker("leads_crm", "can_update"))])
def route_convert_lead_to_customer(data: LeadCreate, db: Session = Depends(get_db)):
    """
    Triggers the ERP script to convert a lead to a customer using provided data.
    """
    return convert_lead_to_customer_erp(data, db)

@router.post("/", response_model=LeadOut, dependencies=[Depends(PermissionChecker("leads_crm", "can_create"))])
def route_create_lead(data: LeadCreate, db: Session = Depends(get_db)):
    return create_lead_controller(data, db)

@router.get("/", response_model=list[LeadOut], dependencies=[Depends(PermissionChecker("leads_crm", "can_view"))])
def route_get_all_leads(status: Optional[str] = None, db: Session = Depends(get_db)):
    return get_all_leads_controller(db, status=status)

@router.get("/{lead_id}", response_model=LeadOut, dependencies=[Depends(PermissionChecker("leads_crm", "can_view"))])
def route_get_lead_by_id(lead_id: str = Path(...), db: Session = Depends(get_db)):
    return get_lead_by_id_controller(lead_id, db)

@router.put("/{lead_id}", response_model=LeadOut, dependencies=[Depends(PermissionChecker("leads_crm", "can_update"))])
def route_update_lead(lead_id: str = Path(...), data: LeadUpdate = None, db: Session = Depends(get_db)):
    return update_lead_controller(lead_id, data, db)

@router.put("/{lead_id}/status", response_model=LeadOut, dependencies=[Depends(PermissionChecker("leads_crm", "can_update"))])
def route_update_lead_status(lead_id: str = Path(...), data: LeadStatusUpdate = None, db: Session = Depends(get_db)):
    if not data or not data.status:
        raise HTTPException(status_code=400, detail="Status is required")
    return update_lead_status_controller(lead_id, data.status, db)

@router.delete("/{lead_id}", dependencies=[Depends(PermissionChecker("leads_crm", "can_delete"))])
def route_delete_lead(lead_id: str, db: Session = Depends(get_db)):
    return delete_lead_controller(lead_id, db)

@router.post("/{lead_id}/approve", response_model=LeadOut, dependencies=[Depends(PermissionChecker("leads_crm", "can_update"))])
def route_approve_lead(lead_id: str, data: LeadApproval, db: Session = Depends(get_db)):
    return approve_lead_controller(lead_id, data, db)
