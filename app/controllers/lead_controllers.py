from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Union
from app.models.lead_models import Lead
from app.schemas.lead_schemas import LeadCreate, LeadUpdate, LeadApproval
import logging
import requests
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from app.services.erp_service import ERPService
import traceback
logger = logging.getLogger("uvicorn.error")

ERP_API_URL = "http://demoerp.muttasilat.ae/api/method/crm_to_erp_universal"
ERP_TOKEN = "token 16fc43415cf6688:c34564758ed716a"

# =====================================================
# ERP COMMON FUNCTIONS
# =====================================================

def sync_to_erp_universal(doctype: str, data: dict, method: str = "POST"):
    try:
        # If we have lead_name or name, ensure it's sent as 'name' for the ERP update
        if "lead_name" in data and "name" not in data:
            data["name"] = data["lead_name"]
            
        payload = {"doctype": doctype, **data}
        # Use jsonable_encoder to handle Decimal and other non-serializable types
        clean_payload = jsonable_encoder({k: v for k, v in payload.items() if v not in (None, "")})
        
        logger.info(f"[ERP SYNC PAYLOAD] Method: {method}, Payload: {clean_payload}")
        
        request_func = requests.post if method.upper() == "POST" else requests.put
        
        response = request_func(
            ERP_API_URL,
            json=clean_payload,
            headers={
                "Authorization": ERP_TOKEN,
                "Content-Type": "application/json",
                "User-Agent": "PostmanRuntime/7.29.2"
            },
            timeout=15
        )
        return {
            "status_code": response.status_code,
            "response": response.json() if response.ok else response.text
        }
    except Exception as e:
        logger.error(f"[ERP SYNC ERROR] {e}")
        return {"status_code": 500, "error": str(e)}

def sync_opportunity_status_to_erp(lead_name: str):
    """
    Dedicated function to update a lead's status to 'Opportunity' in the ERP
    using the universal API method.
    """
    try:
        payload = {
            "doctype": "Lead",
            "name": lead_name,
            "status": "Opportunity"
        }
        # Use jsonable_encoder for consistency and safety
        clean_payload = jsonable_encoder(payload)
        logger.info(f"[ERP OPPORTUNITY SYNC] Sending payload: {clean_payload}")
        
        response = requests.post(
            ERP_API_URL,
            json=clean_payload,
            headers={
                "Authorization": ERP_TOKEN,
                "Content-Type": "application/json"
            },
            timeout=15
        )
        return {
            "status_code": response.status_code,
            "response": response.json() if response.ok else response.text
        }
    except Exception as e:
        logger.error(f"[ERP OPPORTUNITY SYNC ERROR] {e}")
        return {"status_code": 500, "error": str(e)}

def convert_lead_to_customer_erp(data: LeadCreate, db: Session):
    """
    Triggers the ERP script to convert a lead to a customer using provided data.
    """
    url = "http://demoerp.muttasilat.ae/api/method/crm_to_erp_universal"

    try:
        # Mandatory field validation
        if not data.lead_name:
            raise HTTPException(status_code=400, detail="Lead Name is required for ERP sync")
        if not data.customer_name:
            raise HTTPException(status_code=400, detail="Customer Name is required for ERP sync")

        # 1. Save or Update Locally
        lead = db.query(Lead).filter(Lead.lead_name == data.lead_name).first()
        
        lead_data = data.dict(exclude_unset=True)
        # Ensure numeric types are correct
        if 'annual_revenue' in lead_data and lead_data['annual_revenue'] is not None:
            lead_data['annual_revenue'] = float(lead_data['annual_revenue'])

        if lead:
            for key, value in lead_data.items():
                setattr(lead, key, value)
        else:
            lead = Lead(**lead_data)
            db.add(lead)
        
        db.commit()
        db.refresh(lead)

        # 2. Prepare ERP Payload
        payload = {
            "target": "lead",
            "creation": str(data.creation) if data.creation else None,
            "modified": str(data.modified) if data.modified else None,
            "modified_by": data.modified_by,
            "owner": data.owner,
            "first_name": data.first_name,
            "middle_name": data.middle_name,
            "last_name": data.last_name,
            "docstatus": data.docstatus,
            "doctype": data.doctype,
            "idx": data.idx,

            "lead_name": data.lead_name,
            "customer_name": data.customer_name,
            "customer_type": data.customer_type,
            "customer_group": data.customer_group,

            "territory": data.territory,
            "language": data.language,

            "mobile_no": data.mobile_no,
            "email_id": data.email_id,
            "website": data.website,

            "gender": data.gender,
            "industry": data.industry,
            "market_segment": data.market_segment,

            "opportunity_name": data.opportunity_name,
            "account_manager": data.account_manager,

            "default_price_list": data.default_price_list,
            "default_bank_account": data.default_bank_account,
            "default_currency": data.default_currency,

            "is_internal_customer": data.is_internal_customer,
            "represents_company": data.represents_company,

            "customer_pos_id": data.customer_pos_id,
            "customer_details": data.customer_details,
            "customer_primary_contact": data.customer_primary_contact,
            "customer_primary_address": data.customer_primary_address,
            "primary_address": data.primary_address,

            "tax_id": data.tax_id,
            "tax_category": data.tax_category,
            "tax_withholding_category": data.tax_withholding_category,

            "payment_terms": data.payment_terms,
            "loyalty_program": data.loyalty_program,
            "loyalty_program_tier": data.loyalty_program_tier,

            "default_sales_partner": data.default_sales_partner,
            "default_commission_rate": data.default_commission_rate,

            "so_required": data.so_required,
            "dn_required": data.dn_required,
            "is_frozen": data.is_frozen,
            "disabled": data.disabled,

            "custom_ntn_number": data.custom_ntn_number,
            "custom_technical_poc": data.custom_technical_poc,
            "custom_aend_address": data.custom_aend_address,
            "custom_bend_address": data.custom_bend_address,
            "custom_static_ip": data.custom_static_ip,
            "custom_vlan_id": data.custom_vlan_id,
            "custom_handover_point": data.custom_handover_point,
            "custom_bandwidth_type": data.custom_bandwidth_type,
            "custom_aggregated_port_speed": data.custom_aggregated_port_speed
        }

        # remove null values
        payload = {k: v for k, v in payload.items() if v is not None}

        # 3. Handle Products & Contracts Locally first (Ensures data integrity even if ERP is flaky)
        if data.products:
            try:
                ERPService.save_lead_products(db, lead.id, data.products)
            except Exception as pe:
                logger.error(f"Error saving lead products: {pe}")

        if data.contract_template_id:
            try:
                ERPService.generate_contract(db, lead.id, data.contract_template_id)
            except Exception as ce:
                logger.error(f"Error generating contract: {ce}")

        # 4. Sync to ERP using Universal Helper with POST
        erp_res_wrapped = sync_to_erp_universal(data.doctype or "Lead", payload, method="POST")
        erp_res = erp_res_wrapped.get("response", {})
        status_code = erp_res_wrapped.get("status_code", 500)

        if status_code >= 400:
            logger.error(f"ERP Sync Failed: {status_code} - {erp_res}")
            raise HTTPException(
                status_code=status_code if status_code in [400, 401, 403, 404] else 502,
                detail=f"Local data saved, but ERP sync failed: {erp_res}"
            )

        return {
            "status": "success",
            "message": "Lead saved locally and synced to ERP",
            "lead_id": lead.id,
            "erp_response": erp_res
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Internal Error in convert_lead_to_customer_erp: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"CRM Internal Error: {str(e)}"
        )

def get_erp_leads_controller(status: str = "Opportunity"):
    """
    Fetches leads from the ERP Lead ISP CRM resource filtered by status.
    Defaults to 'Opportunity', but also handles related statuses like CAME and Opportunity.
    """
    base_url = "http://demoerp.muttasilat.ae/api/resource/Lead ISP CRM"
    # We use a filter to get any of the relevant statuses
    filters = f"[[\"status\", \"in\", [\"Opportunity\", \"Opportunity\", \"CAME\"]]]"
    params = {
        "fields": "[\"*\"]",
        "filters": filters
    }
    try:
        response = requests.get(
            base_url,
            params=params,
            headers={
                "Authorization": ERP_TOKEN,
                "Content-Type": "application/json"
            },
            timeout=15
        )
        if not response.ok:
            logger.error(f"[ERP FETCH ERROR] Status: {response.status_code}, URL: {response.url}, Response: {response.text}")
            return []
        
        data = response.json().get("data", [])
        return data
    except Exception as e:
        logger.error(f"[ERP FETCH EXCEPTION] {e}")
        return []

def get_erp_lead_by_name_controller(name: str):
    """
    Fetches a single lead from ERP by its name.
    """
    base_url = "http://demoerp.muttasilat.ae/api/resource/Lead ISP CRM"
    params = {
        "filters": f"[[\"name\",\"=\",\"{name}\"]]",
        "fields": "[\"*\"]"
    }
    try:
        response = requests.get(
            base_url,
            params=params,
            headers={
                "Authorization": ERP_TOKEN,
                "Content-Type": "application/json"
            },
            timeout=15
        )
        if not response.ok:
            logger.error(f"[ERP DETAIL FETCH ERROR] Status: {response.status_code}, URL: {response.url}, Response: {response.text}")
            return None
        
        data = response.json().get("data", [])
        return data[0] if data else None
    except Exception as e:
        logger.error(f"[ERP DETAIL FETCH EXCEPTION] {e}")
        return None

def save_erp_lead_locally_controller(data: dict, db: Session):
    """
    Saves or updates an ERP lead into the local CRM database.
    """
    erp_id = data.get("erp_id")
    lead_name = data.get("lead_name") or data.get("customer_name")
    
    # Try to find existing lead by name or custom field
    lead = db.query(Lead).filter(
        (Lead.lead_name == lead_name) | 
        (Lead.represents_company == erp_id)
    ).first()
    
    # Clean data to match Lead model fields
    model_fields = {c.name for c in Lead.__table__.columns}
    clean_data = {k: v for k, v in data.items() if k in model_fields}
    
    # Map ERP fields to CRM fields if they differ
    if "request_type" not in clean_data and "service_type" in data:
        clean_data["request_type"] = data["service_type"]
    
    # Ensure source is ERP
    clean_data["source"] = "ERP"
    clean_data["represents_company"] = erp_id
    
    try:
        # Check for "noc active" logic or special ERP statuses
        # Only force "Opportunity" if current status is a base level status
        current_status = lead.status if lead else None
        is_base_status = current_status in ["Lead", "Open", None] or data.get("status") in ["Opportunity", "CAME"]
        if (data.get("custom_noc_active") == 1 or data.get("noc_active") == 1) and is_base_status:
            clean_data["status"] = "Opportunity"

        if lead:
            # Update existing
            for key, value in clean_data.items():
                if key != "id":
                    setattr(lead, key, value)
        else:
            # Create new
            lead = Lead(**clean_data)
            db.add(lead)
        
        db.commit()
        db.refresh(lead)
        return lead
    except Exception as e:
        db.rollback()
        logger.error(f"[ERP SAVE ERROR] {e}")
        raise HTTPException(status_code=400, detail=str(e))
# =====================================================
# LEAD CONTROLLERS
# =====================================================

def create_lead_controller(data: LeadCreate, db: Session):
    try:
        lead = Lead(**data.dict())
        db.add(lead)
        db.commit()
        db.refresh(lead)

        erp_payload = {c.name: getattr(lead, c.name) for c in Lead.__table__.columns}
        exclude = ["id", "creation", "modified", "created_at", "updated_at"]
        clean_erp = {k: v for k, v in erp_payload.items() if k not in exclude}
        
        sync_to_erp_universal("Lead", clean_erp)
        return lead
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_all_leads_controller(db: Session, status: Optional[str] = None):
    """
    Fetches all leads from both CRM and ERP, ensures they are synced, and returns a unified list.
    Optional status filter can be applied.
    """
    # 1. Fetch from ERP and Sync to Local DB
    # We fetch based on the requested status (defaulting to Opportunity)
    erp_leads = get_erp_leads_controller(status=status or "Opportunity")
    for erp_lead in erp_leads:
        # Prepare data for save_erp_lead_locally_controller
        erp_data = {
            "erp_id": erp_lead.get("name"),
            "lead_name": erp_lead.get("name"),
            "first_name": erp_lead.get("first_name"),
            "customer_name": erp_lead.get("customer_name") or erp_lead.get("lead_name"),
            "status": erp_lead.get("status"),
            "email_id": erp_lead.get("email_id"),
            "mobile_no": erp_lead.get("mobile_no"),
            "custom_ntn_number": erp_lead.get("custom_ntn_number"),
            "custom_technical_poc": erp_lead.get("custom_technical_poc"),
            "custom_aend_address": erp_lead.get("custom_aend_address"),
            "custom_bend_address": erp_lead.get("custom_bend_address"),
            "custom_static_ip": erp_lead.get("custom_static_ip"),
            "custom_vlan_id": erp_lead.get("custom_vlan_id"),
            "custom_handover_point": erp_lead.get("custom_handover_point"),
            "custom_bandwidth_type": erp_lead.get("custom_bandwidth_type"),
            "custom_aggregated_port_speed": erp_lead.get("custom_aggregated_port_speed"),
            "noc_active": erp_lead.get("noc_active"),
            "custom_noc_active": erp_lead.get("custom_noc_active")
        }
        try:
            save_erp_lead_locally_controller(erp_data, db)
        except Exception as e:
            logger.error(f"[SYNC ERROR] Failed to save ERP lead {erp_data.get('erp_id')}: {e}")

    # 2. Fetch all from Local DB
    query = db.query(Lead)
    if status == "Opportunity":
        # Include related statuses in the "Feasibility" stage
        query = query.filter(Lead.status.in_(["Opportunity", "Opportunity", "CAME"]))
    elif status:
        query = query.filter(Lead.status == status)
    
    return query.all()


def get_lead_by_id_controller(lead_id: str, db: Session):
    # 1. Try direct integer lookup
    try:
        int_id = int(lead_id)
        lead = db.query(Lead).filter(Lead.id == int_id).first()
        if lead: return lead
    except ValueError:
        pass

    # 2. Try direct string lookup (lead_name or represents_company)
    lead = db.query(Lead).filter(
        (Lead.lead_name == lead_id) | 
        (Lead.represents_company == lead_id)
    ).first()
    if lead: return lead

    # 3. Try extracting last 4-5 digits if it's an ERP string (as requested)
    import re
    match = re.search(r'(\d+)$', str(lead_id))
    if match:
        extracted_id = int(match.group(1))
        lead = db.query(Lead).filter(Lead.id == extracted_id).first()
        if lead: return lead

    raise HTTPException(status_code=404, detail="Lead not found")

def sync_to_erp_put(lead_name: str, data: dict):
    """
    Calls the ERP PUT API to update a lead based on lead_name.
    """
    if not lead_name:
        return {"status_code": 400, "error": "lead_name is required for PUT sync"}
        
    url = f"http://demoerp.muttasilat.ae/api/resource/Lead ISP CRM/{lead_name}"
    try:
        # Use jsonable_encoder to handle Decimal and other non-serializable types
        clean_payload = jsonable_encoder({k: v for k, v in data.items() if v not in (None, "")})
        logger.info(f"[ERP PUT SYNC] Updating {lead_name} with data: {clean_payload}")
        response = requests.put(
            url,
            json=clean_payload,
            headers={
                "Authorization": ERP_TOKEN,
                "Content-Type": "application/json"
            },
            timeout=15
        )
        logger.info(f"[ERP PUT SYNC] Response: {response.status_code} - {response.text}")
        return {
            "status_code": response.status_code,
            "response": response.json() if response.ok else response.text
        }
    except Exception as e:
        logger.error(f"[ERP PUT SYNC ERROR] {e}")
        return {"status_code": 500, "error": str(e)}

def update_lead_controller(lead_id: str, data: LeadUpdate, db: Session):
    try:
        lead = get_lead_by_id_controller(lead_id, db)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        update_data = data.dict(exclude_unset=True)
        
        # Implement "noc active" logic
        # Only force "Opportunity" if the status is currently "Lead" or "Open"
        # and NOC is active. This prevents stuck status for leads already in progress.
        if (update_data.get("noc_active") or update_data.get("custom_noc_active")) and lead.status in ["Lead", "Open", None]:
             update_data["status"] = "Opportunity"

        # Explicitly handle status update if present in update_data
        if "status" in update_data:
             logger.info(f"[UPDATE LEAD] Explicitly setting status from {lead.status} to {update_data['status']}")
             lead.status = update_data["status"]

        for key, value in update_data.items():
            if hasattr(lead, key) and key != "id" and key != "status":
                setattr(lead, key, value)
    
        db.commit()
        db.refresh(lead)
        logger.info(f"[UPDATE LEAD] Database commit successful. New DB status: {lead.status}")

        # Sync to ERP using PUT if lead_name exists, otherwise fallback to POST
        erp_payload = {c.name: getattr(lead, c.name) for c in Lead.__table__.columns}
        exclude = ["id", "creation", "modified", "created_at", "updated_at"]
        clean_erp = {k: v for k, v in erp_payload.items() if k not in exclude}
        
        # Map internal status back to ERP status
        if clean_erp.get("status") == "Opportunity":
            clean_erp["status"] = "Opportunity"
        
        if lead.lead_name:
            sync_res = sync_to_erp_universal("Lead", clean_erp, method="PUT")
            logger.info(f"[UPDATE LEAD] ERP Universal Sync Result: {sync_res}")
        else:
            sync_res = sync_to_erp_universal("Lead", clean_erp, method="PUT")
            logger.info(f"[UPDATE LEAD] ERP Universal Sync Result: {sync_res}")

        return lead
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete_lead_controller(lead_id: str, db: Session):
    try:
        lead = get_lead_by_id_controller(lead_id, db)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        db.delete(lead)
        db.commit()
        return {"message": "Lead deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def approve_lead_controller(lead_id: str, data: LeadApproval, db: Session):
    try:
        lead = get_lead_by_id_controller(lead_id, db)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        lead.status = "Approved" if data.action.lower() == "approve" else "Rejected"
        db.commit()
        db.refresh(lead)

        # Sync approval status to ERP
        if lead.lead_name:
            erp_payload = {c.name: getattr(lead, c.name) for c in Lead.__table__.columns}
            exclude = ["id", "creation", "modified", "created_at", "updated_at"]
            clean_erp = {k: v for k, v in erp_payload.items() if k not in exclude}

            # Map internal status back to ERP status
            if clean_erp.get("status") == "Opportunity":
                clean_erp["status"] = "Opportunity"

            sync_res = sync_to_erp_universal("Lead", clean_erp, method="PUT")
            logger.info(f"[APPROVE LEAD] ERP Universal Sync Result: {sync_res}")

        return lead
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def update_lead_status_controller(lead_id: str, status: str, db: Session):
    try:
        lead = get_lead_by_id_controller(lead_id, db)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        # 1. Update Locally first
        old_status = lead.status
        lead.status = status
        db.commit()
        db.refresh(lead)
        
        logger.info(f"[STATUS UPDATE] Lead {lead_id} ({lead.lead_name}) changed from {old_status} to {status}")
        
        # 2. Sync to ERP
        if lead.lead_name:
            erp_payload = {c.name: getattr(lead, c.name) for c in Lead.__table__.columns}
            exclude = ["id", "creation", "modified", "created_at", "updated_at"]
            clean_erp = {k: v for k, v in erp_payload.items() if k not in exclude}
            
            # Ensure the new status is in the payload
            clean_erp["status"] = status
            
            # Map for ERP consistency - if it's a specific status the ERP expects
            if status == "Opportunity":
                # Call the dedicated Opportunity sync function
                sync_res = sync_opportunity_status_to_erp(lead.lead_name)
                logger.info(f"[STATUS UPDATE] Dedicated Opportunity Sync Result: {sync_res}")
            else:
                # Call Universal API with PUT for other statuses
                sync_res = sync_to_erp_universal("Lead", clean_erp, method="PUT")
                logger.info(f"[STATUS UPDATE] ERP Universal Sync ({lead.lead_name}): {sync_res}")
            
            # Also call Standard Resource PUT Sync for redundancy/fallback
            try:
                sync_res_put = sync_to_erp_put(lead.lead_name, clean_erp)
                logger.info(f"[STATUS UPDATE] ERP Standard Sync ({lead.lead_name}): {sync_res_put}")
            except Exception as put_e:
                logger.error(f"[STATUS UPDATE] ERP Standard Sync Failed: {put_e}")
            
        return lead
    except Exception as e:
        db.rollback()
        logger.error(f"[STATUS UPDATE ERROR] {e}")
        raise HTTPException(status_code=400, detail=str(e))